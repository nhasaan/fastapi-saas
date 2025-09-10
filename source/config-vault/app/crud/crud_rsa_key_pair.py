from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rsa_key_pair import RSAKeyPair
from app.schemas.rsa_key_pair import RSAKeyPairCreate, RSAKeyPairUpdate

class CRUDRSAKeyPair(CRUDBase[RSAKeyPair, RSAKeyPairCreate, RSAKeyPairUpdate]):
    def get_by_kid(self, db: Session, *, kid: str) -> Optional[RSAKeyPair]:
        return db.query(RSAKeyPair).filter(RSAKeyPair.kid == kid).first()
    
    def get_by_tenant_id(self, db: Session, *, tenant_id: Union[UUID, str]) -> List[RSAKeyPair]:
        return db.query(RSAKeyPair).filter(RSAKeyPair.tenant_id == tenant_id).all()
    
    def get_by_site_id(self, db: Session, *, site_id: Union[UUID, str]) -> List[RSAKeyPair]:
        return db.query(RSAKeyPair).filter(RSAKeyPair.site_id == site_id).all()
    
    def get_active_by_tenant_id(self, db: Session, *, tenant_id: Union[UUID, str]) -> List[RSAKeyPair]:
        return db.query(RSAKeyPair).filter(
            RSAKeyPair.tenant_id == tenant_id,
            RSAKeyPair.status == "active"
        ).all()
    
    def get_active_by_site_id(self, db: Session, *, site_id: Union[UUID, str]) -> List[RSAKeyPair]:
        return db.query(RSAKeyPair).filter(
            RSAKeyPair.site_id == site_id,
            RSAKeyPair.status == "active"
        ).all()
    
    def update_status(self, db: Session, *, id: Union[UUID, str], status: str) -> Optional[RSAKeyPair]:
        db_obj = db.query(RSAKeyPair).filter(RSAKeyPair.id == id).first()
        if db_obj:
            db_obj.status = status
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

rsa_key_pair = CRUDRSAKeyPair(RSAKeyPair)
