from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: str
    client_name: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    is_featured: bool = False
    order: int = 0
    is_active: bool = True
    completed_at: Optional[date] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    client_name: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    is_featured: Optional[bool] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None
    completed_at: Optional[date] = None


class ProjectOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    client_name: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    is_featured: bool
    order: int
    is_active: bool
    completed_at: Optional[date] = None
    created_at: datetime

    model_config = {"from_attributes": True}
