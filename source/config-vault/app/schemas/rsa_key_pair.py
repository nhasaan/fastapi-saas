from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class RSAKeyPairBase(BaseModel):
    tenant_id: UUID
    site_id: Optional[UUID] = None
    expires_in_days: int = 365

class RSAKeyPairCreate(RSAKeyPairBase):
    pass

class RSAKeyPairInDBBase(BaseModel):
    id: UUID
    kid: str
    public_key: str
    tenant_id: UUID
    site_id: Optional[UUID] = None
    status: str
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class RSAKeyPair(RSAKeyPairInDBBase):
    pass

class RSAKeyPairWithPrivate(RSAKeyPairInDBBase):
    private_key: str

class RSAKeyPairInDB(RSAKeyPairInDBBase):
    private_key: str
