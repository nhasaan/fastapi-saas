from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class TenantBase(BaseModel):
    name: str
    domain: str
    is_active: bool = True

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None

class TenantInDBBase(TenantBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class Tenant(TenantInDBBase):
    pass

class TenantInDB(TenantInDBBase):
    pass
