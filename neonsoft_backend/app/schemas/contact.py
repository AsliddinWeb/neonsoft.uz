from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContactCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str
    source: Optional[str] = 'contact'


class ContactOut(BaseModel):
    id: int
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str
    source: str = 'contact'
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
