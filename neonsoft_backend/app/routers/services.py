from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.service import Service
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceOut, ServiceUpdate
from app.utils.slug import generate_unique_slug

public_router = APIRouter(prefix="/api/services", tags=["Services"])
admin_router = APIRouter(prefix="/api/admin/services", tags=["Admin - Services"])


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.get("", response_model=List[ServiceOut])
async def list_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Service).where(Service.is_active == True).order_by(Service.order)
    )
    return result.scalars().all()


@public_router.get("/{slug}", response_model=ServiceOut)
async def get_service(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Service).where(Service.slug == slug, Service.is_active == True)
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=List[ServiceOut])
async def admin_list_services(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Service).order_by(Service.order))
    return result.scalars().all()


@admin_router.post("", response_model=ServiceOut, status_code=201)
async def create_service(
    data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    slug = await generate_unique_slug(db, Service, data.title)
    service = Service(**data.model_dump(), slug=slug)
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


@admin_router.put("/{service_id}", response_model=ServiceOut)
async def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = data.model_dump(exclude_unset=True)
    if "title" in update_data:
        update_data["slug"] = await generate_unique_slug(
            db, Service, update_data["title"], exclude_id=service_id
        )

    for key, value in update_data.items():
        setattr(service, key, value)

    await db.commit()
    await db.refresh(service)
    return service


@admin_router.delete("/{service_id}", status_code=204)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    await db.delete(service)
    await db.commit()
