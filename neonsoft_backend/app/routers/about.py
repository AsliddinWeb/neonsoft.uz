from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.about import About
from app.models.user import User
from app.schemas.about import AboutOut, AboutUpdate

public_router = APIRouter(prefix="/api/about", tags=["About"])
admin_router = APIRouter(prefix="/api/admin/about", tags=["Admin - About"])


async def get_or_create_about(db: AsyncSession) -> About:
    result = await db.execute(select(About))
    about = result.scalar_one_or_none()
    if not about:
        about = About(
            title="Biz haqimizda",
            subtitle="NeonSoft — raqamli kelajakni birga quramiz",
            description="NeonSoft — zamonaviy IT yechimlar yaratuvchi o'zbek kompaniyasi.",
            stat_projects=50,
            stat_clients=30,
            stat_years=5,
            stat_team=15,
        )
        db.add(about)
        await db.commit()
        await db.refresh(about)
    return about


@public_router.get("", response_model=AboutOut)
async def get_about(db: AsyncSession = Depends(get_db)):
    return await get_or_create_about(db)


@admin_router.get("", response_model=AboutOut)
async def admin_get_about(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await get_or_create_about(db)


@admin_router.put("", response_model=AboutOut)
async def update_about(
    data: AboutUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    about = await get_or_create_about(db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(about, key, value)
    await db.commit()
    await db.refresh(about)
    return about