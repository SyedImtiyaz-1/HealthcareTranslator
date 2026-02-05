import os
import uuid
import aiofiles
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_audio(file_content: bytes, filename: str) -> str:
    file_extension = Path(filename).suffix or ".webm"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file_content)
    
    return unique_filename


def get_audio_path(filename: str) -> Path:
    return UPLOAD_DIR / filename


def delete_audio(filename: str) -> bool:
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False
