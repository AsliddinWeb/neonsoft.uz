from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.blog import BlogPost
from app.models.user import User
from app.schemas.blog import BlogPostCreate, BlogPostList, BlogPostOut, BlogPostUpdate
from app.utils.slug import generate_unique_slug

public_router = APIRouter(prefix="/api/blog", tags=["Blog"])
admin_router = APIRouter(prefix="/api/admin/blog", tags=["Admin - Blog"])


# ─── Public ───────────────────────────────────────────────────────────────────

@public_router.get("", response_model=List[BlogPostList])
async def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    tag: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(BlogPost).where(BlogPost.is_published == True)
    if tag:
        # PostgreSQL: 'tag' = ANY(tags)
        query = query.where(BlogPost.tags.any(tag))
    query = (
        query.order_by(BlogPost.published_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@public_router.get("/{slug}", response_model=BlogPostOut)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BlogPost).where(BlogPost.slug == slug, BlogPost.is_published == True)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Increment views atomically
    await db.execute(
        update(BlogPost).where(BlogPost.id == post.id).values(views=BlogPost.views + 1)
    )
    await db.commit()
    await db.refresh(post)
    return post


# ─── Admin ────────────────────────────────────────────────────────────────────

@admin_router.get("", response_model=List[BlogPostList])
async def admin_list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = (
        select(BlogPost)
        .order_by(BlogPost.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@admin_router.post("", response_model=BlogPostOut, status_code=201)
async def create_post(
    data: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = await generate_unique_slug(db, BlogPost, data.title)
    post_data = data.model_dump()
    published_at = None
    if post_data.get("is_published"):
        published_at = datetime.now(timezone.utc)

    post = BlogPost(**post_data, slug=slug, author_id=current_user.id, published_at=published_at)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@admin_router.put("/{post_id}", response_model=BlogPostOut)
async def update_post(
    post_id: int,
    data: BlogPostUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = data.model_dump(exclude_unset=True)
    if "title" in update_data:
        update_data["slug"] = await generate_unique_slug(
            db, BlogPost, update_data["title"], exclude_id=post_id
        )

    # Auto-set published_at when publishing for the first time
    if update_data.get("is_published") and not post.published_at:
        update_data["published_at"] = datetime.now(timezone.utc)

    for key, value in update_data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post


@admin_router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
