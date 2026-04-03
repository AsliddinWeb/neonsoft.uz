from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SiteSettingUpdate(BaseModel):
    company_name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None


class SiteSettingOut(BaseModel):
    id: int
    company_name: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    telegram: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
