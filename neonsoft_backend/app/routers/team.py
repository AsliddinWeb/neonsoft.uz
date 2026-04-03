from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.team_member import TeamMember
from app.models.user import User
from app.schemas.team_member import TeamMemberCreate, TeamMemberOut, TeamMemberUpdate

public_router = APIRouter(prefix="/api/team", tags=["Team"])
admin_router = APIRouter(prefix="/api/admin/team", tags=["Admin - Team"])


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.get("", response_model=List[TeamMemberOut])
async def list_team(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TeamMember).where(TeamMember.is_active == True).order_by(TeamMember.order)
    )
    return result.scalars().all()


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=List[TeamMemberOut])
async def admin_list_team(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(TeamMember).order_by(TeamMember.order))
    return result.scalars().all()


@admin_router.post("", response_model=TeamMemberOut, status_code=201)
async def create_member(
    data: TeamMemberCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    member = TeamMember(**data.model_dump())
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@admin_router.put("/{member_id}", response_model=TeamMemberOut)
async def update_member(
    member_id: int,
    data: TeamMemberUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(TeamMember).where(TeamMember.id == member_id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(member, key, value)

    await db.commit()
    await db.refresh(member)
    return member


@admin_router.delete("/{member_id}", status_code=204)
async def delete_member(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(TeamMember).where(TeamMember.id == member_id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    await db.delete(member)
    await db.commit()
