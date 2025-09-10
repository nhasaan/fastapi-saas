from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.base_class import Base

class RSAKeyPair(Base):
    __tablename__ = "rsa_key_pairs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    kid = Column(String(255), unique=True, nullable=False, index=True)
    private_key = Column(Text, nullable=False)
    public_key = Column(Text, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=True)  # None for tenant-level keys
    status = Column(String(50), default="active")
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="rsa_keys")
    site = relationship("Site", back_populates="rsa_keys")
