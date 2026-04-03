from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ServiceCreate(BaseModel):
    title: str
    short_description: str
    description: str
    icon: Optional[str] = None
    order: int = 0
    is_active: bool = True


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class ServiceOut(BaseModel):
    id: int
    title: str
    slug: str
    short_description: str
    description: str
    icon: Optional[str] = None
    order: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
