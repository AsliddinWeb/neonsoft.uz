from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.contact import ContactMessage
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactOut

public_router = APIRouter(prefix="/api/contact", tags=["Contact"])
admin_router = APIRouter(prefix="/api/admin/contacts", tags=["Admin - Contacts"])


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.post("", response_model=ContactOut, status_code=201)
async def send_message(data: ContactCreate, db: AsyncSession = Depends(get_db)):
    message = ContactMessage(**data.model_dump())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=List[ContactOut])
async def list_messages(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = (
        select(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@admin_router.patch("/{message_id}/read", response_model=ContactOut)
async def mark_read(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(ContactMessage).where(ContactMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.is_read = True
    await db.commit()
    await db.refresh(message)
    return message


@admin_router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(ContactMessage).where(ContactMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    await db.delete(message)
    await db.commit()
