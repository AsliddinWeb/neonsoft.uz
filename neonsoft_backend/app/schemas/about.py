from typing import Optional
from pydantic import BaseModel


class AboutUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    stat_projects: Optional[int] = None
    stat_clients: Optional[int] = None
    stat_years: Optional[int] = None
    stat_team: Optional[int] = None


class AboutOut(BaseModel):
    id: int
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    stat_projects: int = 0
    stat_clients: int = 0
    stat_years: int = 0
    stat_team: int = 0

    model_config = {"from_attributes": True}