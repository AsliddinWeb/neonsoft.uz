from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.user import UserOut


class BlogPostCreate(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: bool = False


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None


class BlogPostOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: bool
    views: int
    author: UserOut
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BlogPostList(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    cover_image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: bool
    views: int
    author: UserOut
    published_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
