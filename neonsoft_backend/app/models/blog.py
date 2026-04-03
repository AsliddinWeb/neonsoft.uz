from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    author: Mapped["User"] = relationship("User", lazy="selectin")
