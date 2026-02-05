from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.connection import get_db
from database.models import Conversation, Message, Summary
from services.summarization import generate_summary
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/summary", tags=["summary"])


class SummaryResponse(BaseModel):
    id: str
    conversation_id: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/conversations/{conversation_id}")
async def create_summary(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages), selectinload(Conversation.summary))
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if not conversation.messages:
        raise HTTPException(status_code=400, detail="No messages to summarize")
    
    messages_data = [
        {
            "role": msg.role.value,
            "original_text": msg.original_text,
            "translated_text": msg.translated_text
        }
        for msg in sorted(conversation.messages, key=lambda m: m.created_at)
    ]
    
    summary_content = await generate_summary(messages_data)
    
    if conversation.summary:
        conversation.summary.content = summary_content
        conversation.summary.created_at = datetime.utcnow()
        summary = conversation.summary
    else:
        summary = Summary(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=summary_content
        )
        db.add(summary)
    
    await db.commit()
    await db.refresh(summary)
    
    return SummaryResponse(
        id=summary.id,
        conversation_id=summary.conversation_id,
        content=summary.content,
        created_at=summary.created_at
    )


@router.get("/conversations/{conversation_id}")
async def get_summary(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Summary).where(Summary.conversation_id == conversation_id)
    )
    summary = result.scalar_one_or_none()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return SummaryResponse(
        id=summary.id,
        conversation_id=summary.conversation_id,
        content=summary.content,
        created_at=summary.created_at
    )
