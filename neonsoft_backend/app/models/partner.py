from typing import Optional

from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Partner(Base):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    website_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)