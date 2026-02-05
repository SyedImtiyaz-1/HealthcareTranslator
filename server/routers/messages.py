from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.connection import get_db
from database.models import Conversation, Message, RoleType
from services.translation import translate_text
from websocket.manager import manager
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/messages", tags=["messages"])


class MessageCreate(BaseModel):
    conversation_id: str
    role: str
    original_text: str
    source_language: str
    target_language: str
    audio_path: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    audio_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("", response_model=MessageResponse)
async def create_message(message_data: MessageCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation).where(Conversation.id == message_data.conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    translated_text = await translate_text(
        message_data.original_text,
        message_data.source_language,
        message_data.target_language
    )
    
    role_enum = RoleType.DOCTOR if message_data.role.lower() == "doctor" else RoleType.PATIENT
    
    message = Message(
        id=str(uuid.uuid4()),
        conversation_id=message_data.conversation_id,
        role=role_enum,
        original_text=message_data.original_text,
        translated_text=translated_text,
        source_language=message_data.source_language,
        target_language=message_data.target_language,
        audio_path=message_data.audio_path
    )
    
    db.add(message)
    conversation.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(message)
    
    message_broadcast = {
        "type": "new_message",
        "data": {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "role": message.role.value,
            "original_text": message.original_text,
            "translated_text": message.translated_text,
            "source_language": message.source_language,
            "target_language": message.target_language,
            "audio_path": message.audio_path,
            "created_at": message.created_at.isoformat()
        }
    }
    await manager.broadcast(message_data.conversation_id, message_broadcast)
    
    return MessageResponse(
        id=message.id,
        conversation_id=message.conversation_id,
        role=message.role.value,
        original_text=message.original_text,
        translated_text=message.translated_text,
        source_language=message.source_language,
        target_language=message.target_language,
        audio_path=message.audio_path,
        created_at=message.created_at
    )


@router.get("/conversation/{conversation_id}")
async def get_conversation_messages(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    return [
        {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "role": msg.role.value,
            "original_text": msg.original_text,
            "translated_text": msg.translated_text,
            "source_language": msg.source_language,
            "target_language": msg.target_language,
            "audio_path": msg.audio_path,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
