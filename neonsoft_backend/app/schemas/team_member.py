from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TeamMemberCreate(BaseModel):
    full_name: str
    position: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    telegram_url: Optional[str] = None
    order: int = 0
    is_active: bool = True


class TeamMemberUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    telegram_url: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class TeamMemberOut(BaseModel):
    id: int
    full_name: str
    position: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    telegram_url: Optional[str] = None
    order: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
