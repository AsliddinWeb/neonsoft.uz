from typing import Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class About(Base):
    __tablename__ = "about"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subtitle: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    stat_projects: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stat_clients: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stat_years: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stat_team: Mapped[int] = mapped_column(Integer, default=0, nullable=False)