from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate

class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    def get_by_domain(self, db: Session, *, domain: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.domain == domain).first()

tenant = CRUDTenant(Tenant)
