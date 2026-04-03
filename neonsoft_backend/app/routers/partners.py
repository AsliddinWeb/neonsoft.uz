from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.partner import Partner
from app.models.user import User
from app.schemas.partner import PartnerCreate, PartnerOut, PartnerUpdate

public_router = APIRouter(prefix="/api/partners", tags=["Partners"])
admin_router = APIRouter(prefix="/api/admin/partners", tags=["Admin - Partners"])


@public_router.get("", response_model=List[PartnerOut])
async def list_partners(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Partner).where(Partner.is_active == True).order_by(Partner.order)
    )
    return result.scalars().all()


@admin_router.get("", response_model=List[PartnerOut])
async def admin_list_partners(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Partner).order_by(Partner.order))
    return result.scalars().all()


@admin_router.post("", response_model=PartnerOut, status_code=201)
async def create_partner(
    data: PartnerCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    partner = Partner(**data.model_dump())
    db.add(partner)
    await db.commit()
    await db.refresh(partner)
    return partner


@admin_router.put("/{partner_id}", response_model=PartnerOut)
async def update_partner(
    partner_id: int,
    data: PartnerUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Partner).where(Partner.id == partner_id))
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(partner, key, value)
    await db.commit()
    await db.refresh(partner)
    return partner


@admin_router.delete("/{partner_id}", status_code=204)
async def delete_partner(
    partner_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Partner).where(Partner.id == partner_id))
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    await db.delete(partner)
    await db.commit()