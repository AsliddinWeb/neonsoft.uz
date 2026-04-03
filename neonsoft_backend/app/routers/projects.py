from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.utils.slug import generate_unique_slug

public_router = APIRouter(prefix="/api/projects", tags=["Projects"])
admin_router = APIRouter(prefix="/api/admin/projects", tags=["Admin - Projects"])


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.get("", response_model=List[ProjectOut])
async def list_projects(
    featured: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    query = select(Project).where(Project.is_active == True)
    if featured is not None:
        query = query.where(Project.is_featured == featured)
    query = query.order_by(Project.order).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@public_router.get("/{slug}", response_model=ProjectOut)
async def get_project(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project).where(Project.slug == slug, Project.is_active == True)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=List[ProjectOut])
async def admin_list_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = select(Project).order_by(Project.order).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@admin_router.post("", response_model=ProjectOut, status_code=201)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    slug = await generate_unique_slug(db, Project, data.title)
    project = Project(**data.model_dump(), slug=slug)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@admin_router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = data.model_dump(exclude_unset=True)
    if "title" in update_data:
        update_data["slug"] = await generate_unique_slug(
            db, Project, update_data["title"], exclude_id=project_id
        )

    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


@admin_router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
