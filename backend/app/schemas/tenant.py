from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class TenantBase(BaseModel):
    name: str
    country: str
    branding_config: Dict = {}

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
