from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate

class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):
    def get_by_domain(self, db: Session, *, domain: str) -> Optional[Site]:
        return db.query(Site).filter(Site.domain == domain).first()
    
    def get_by_tenant_id(self, db: Session, *, tenant_id: Union[UUID, str]) -> List[Site]:
        return db.query(Site).filter(Site.tenant_id == tenant_id).all()

site = CRUDSite(Site)
