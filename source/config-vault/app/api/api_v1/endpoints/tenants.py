from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.api import deps
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate

router = APIRouter()

@router.post("/", response_model=Tenant)
def create_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: TenantCreate,
) -> Tenant:
    """
    Create new tenant.
    """
    # Check if domain already exists
    tenant = crud.tenant.get_by_domain(db, domain=tenant_in.domain)
    if tenant:
        raise HTTPException(
            status_code=400,
            detail="A tenant with this domain already exists in the system.",
        )
    tenant = crud.tenant.create(db=db, obj_in=tenant_in)
    return tenant

@router.get("/", response_model=List[Tenant])
def read_tenants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Tenant]:
    """
    Retrieve tenants.
    """
    tenants = crud.tenant.get_multi(db, skip=skip, limit=limit)
    return tenants

@router.get("/{tenant_id}", response_model=Tenant)
def read_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID,
) -> Tenant:
    """
    Get tenant by ID.
    """
    tenant = crud.tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=Tenant)
def update_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID,
    tenant_in: TenantUpdate,
) -> Tenant:
    """
    Update a tenant.
    """
    tenant = crud.tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check if new domain already exists
    if tenant_in.domain:
        existing_tenant = crud.tenant.get_by_domain(db, domain=tenant_in.domain)
        if existing_tenant and existing_tenant.id != tenant_id:
            raise HTTPException(
                status_code=400,
                detail="A tenant with this domain already exists in the system.",
            )
    
    tenant = crud.tenant.update(db=db, db_obj=tenant, obj_in=tenant_in)
    return tenant

@router.delete("/{tenant_id}", response_model=Tenant)
def delete_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID,
) -> Tenant:
    """
    Delete a tenant.
    """
    tenant = crud.tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant = crud.tenant.remove(db=db, id=tenant_id)
    return tenant
