from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SiteBase(BaseModel):
    name: str
    domain: str
    tenant_id: UUID
    is_active: bool = True

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None

class SiteInDBBase(SiteBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class Site(SiteInDBBase):
    pass

class SiteInDB(SiteInDBBase):
    pass
