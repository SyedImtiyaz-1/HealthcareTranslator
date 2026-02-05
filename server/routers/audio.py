from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.connection import get_db
from database.models import Message
from services.audio import save_audio, get_audio_path
from pydantic import BaseModel

router = APIRouter(prefix="/audio", tags=["audio"])


class AudioUploadResponse(BaseModel):
    filename: str
    message: str


@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    message_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    filename = await save_audio(content, file.filename)
    
    if message_id:
        result = await db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalar_one_or_none()
        if message:
            message.audio_path = filename
            await db.commit()
    
    return AudioUploadResponse(
        filename=filename,
        message="Audio uploaded successfully"
    )


@router.get("/{filename}")
async def get_audio(filename: str):
    file_path = get_audio_path(filename)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/webm",
        filename=filename
    )
