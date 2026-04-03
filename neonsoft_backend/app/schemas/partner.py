from typing import Optional
from pydantic import BaseModel


class PartnerCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    order: int = 0
    is_active: bool = True


class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class PartnerOut(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    order: int
    is_active: bool

    model_config = {"from_attributes": True}