from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tagline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    telegram: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    instagram: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    github: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_keywords: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
