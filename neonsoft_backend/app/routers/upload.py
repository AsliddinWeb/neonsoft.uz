import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.config import settings
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/upload", tags=["Upload"])

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/svg+xml",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class UploadResponse(BaseModel):
    url: str


@router.post("/image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: {file.content_type}. Allowed: jpeg, png, webp, gif, svg",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=422, detail="File too large. Maximum size is 10 MB.")

    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    filepath = os.path.join(settings.MEDIA_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    return UploadResponse(url=f"{settings.MEDIA_URL}/{filename}")
