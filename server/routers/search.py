from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from database.connection import get_db
from database.models import Message, Conversation
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    message_id: str
    conversation_id: str
    role: str
    original_text: str
    translated_text: str
    created_at: str
    match_context: str


@router.get("", response_model=List[SearchResult])
async def search_conversations(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    search_term = f"%{q.lower()}%"
    
    result = await db.execute(
        select(Message)
        .where(
            or_(
                Message.original_text.ilike(search_term),
                Message.translated_text.ilike(search_term)
            )
        )
        .order_by(Message.created_at.desc())
        .limit(50)
    )
    messages = result.scalars().all()
    
    results = []
    for msg in messages:
        text = msg.original_text or msg.translated_text or ""
        q_lower = q.lower()
        text_lower = text.lower()
        
        start_idx = text_lower.find(q_lower)
        if start_idx != -1:
            context_start = max(0, start_idx - 30)
            context_end = min(len(text), start_idx + len(q) + 30)
            context = text[context_start:context_end]
            if context_start > 0:
                context = "..." + context
            if context_end < len(text):
                context = context + "..."
        else:
            context = text[:60] + "..." if len(text) > 60 else text
        
        results.append(SearchResult(
            message_id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role.value,
            original_text=msg.original_text or "",
            translated_text=msg.translated_text or "",
            created_at=msg.created_at.isoformat(),
            match_context=context
        ))
    
    return results
