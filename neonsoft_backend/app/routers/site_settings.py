from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.site_setting import SiteSetting
from app.models.user import User
from app.schemas.site_setting import SiteSettingOut, SiteSettingUpdate

public_router = APIRouter(prefix="/api/settings", tags=["Site Settings"])
admin_router = APIRouter(prefix="/api/admin/settings", tags=["Admin - Site Settings"])


async def get_or_create_settings(db: AsyncSession) -> SiteSetting:
    result = await db.execute(select(SiteSetting))
    setting = result.scalar_one_or_none()
    if not setting:
        setting = SiteSetting(company_name="NeonSoft")
        db.add(setting)
        await db.commit()
        await db.refresh(setting)
    return setting


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.get("", response_model=SiteSettingOut)
async def get_settings(db: AsyncSession = Depends(get_db)):
    return await get_or_create_settings(db)


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=SiteSettingOut)
async def admin_get_settings(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await get_or_create_settings(db)


@admin_router.put("", response_model=SiteSettingOut)
async def update_settings(
    data: SiteSettingUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    setting = await get_or_create_settings(db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(setting, key, value)
    await db.commit()
    await db.refresh(setting)
    return setting
