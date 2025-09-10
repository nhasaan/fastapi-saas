from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.api import deps
from app.schemas.rsa_key_pair import RSAKeyPair, RSAKeyPairCreate, RSAKeyPairWithPrivate
from app.core.key_generation import KeyGenerationService

router = APIRouter()

@router.post("/", response_model=RSAKeyPairWithPrivate)
def create_rsa_key(
    *,
    db: Session = Depends(deps.get_db),
    key_in: RSAKeyPairCreate,
) -> RSAKeyPairWithPrivate:
    """
    Create new RSA key pair.
    """
    # Verify tenant exists
    tenant = crud.tenant.get(db=db, id=key_in.tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=400,
            detail="The tenant with this ID does not exist in the system.",
        )
    
    # Verify site exists if provided
    if key_in.site_id:
        site = crud.site.get(db=db, id=key_in.site_id)
        if not site:
            raise HTTPException(
                status_code=400,
                detail="The site with this ID does not exist in the system.",
            )
    
    # Generate key pair
    private_key, public_key = KeyGenerationService.generate_rsa_key_pair()
    kid = KeyGenerationService.generate_kid()
    expires_at = KeyGenerationService.calculate_expires_at(key_in.expires_in_days)
    
    # Create key pair object
    key_data = {
        "kid": kid,
        "private_key": private_key,
        "public_key": public_key,
        "tenant_id": key_in.tenant_id,
        "site_id": key_in.site_id,
        "status": "active",
        "expires_at": expires_at
    }
    
    key_pair = crud.rsa_key_pair.create(db=db, obj_in=key_data)
    return key_pair

@router.get("/{kid}", response_model=RSAKeyPair)
def read_rsa_key_by_kid(
    *,
    db: Session = Depends(deps.get_db),
    kid: str,
) -> RSAKeyPair:
    """
    Get RSA key pair by Key ID.
    """
    key_pair = crud.rsa_key_pair.get_by_kid(db=db, kid=kid)
    if not key_pair:
        raise HTTPException(status_code=404, detail="RSA key pair not found")
    return key_pair

@router.get("/tenant/{tenant_id}", response_model=List[RSAKeyPair])
def read_rsa_keys_by_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID,
) -> List[RSAKeyPair]:
    """
    Get RSA key pairs by tenant ID.
    """
    key_pairs = crud.rsa_key_pair.get_by_tenant_id(db=db, tenant_id=tenant_id)
    return key_pairs

@router.get("/site/{site_id}", response_model=List[RSAKeyPair])
def read_rsa_keys_by_site(
    *,
    db: Session = Depends(deps.get_db),
    site_id: UUID,
) -> List[RSAKeyPair]:
    """
    Get RSA key pairs by site ID.
    """
    key_pairs = crud.rsa_key_pair.get_by_site_id(db=db, site_id=site_id)
    return key_pairs

@router.get("/tenant/{tenant_id}/active", response_model=List[RSAKeyPair])
def read_active_rsa_keys_by_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: UUID,
) -> List[RSAKeyPair]:
    """
    Get active RSA key pairs by tenant ID.
    """
    key_pairs = crud.rsa_key_pair.get_active_by_tenant_id(db=db, tenant_id=tenant_id)
    return key_pairs

@router.get("/site/{site_id}/active", response_model=List[RSAKeyPair])
def read_active_rsa_keys_by_site(
    *,
    db: Session = Depends(deps.get_db),
    site_id: UUID,
) -> List[RSAKeyPair]:
    """
    Get active RSA key pairs by site ID.
    """
    key_pairs = crud.rsa_key_pair.get_active_by_site_id(db=db, site_id=site_id)
    return key_pairs

@router.post("/{key_id}/revoke")
def revoke_rsa_key(
    *,
    db: Session = Depends(deps.get_db),
    key_id: UUID,
):
    """
    Revoke an RSA key pair.
    """
    key_pair = crud.rsa_key_pair.update_status(db=db, id=key_id, status="revoked")
    if not key_pair:
        raise HTTPException(status_code=404, detail="RSA key pair not found")
    return {"message": "RSA key pair revoked successfully"}

@router.post("/{key_id}/activate")
def activate_rsa_key(
    *,
    db: Session = Depends(deps.get_db),
    key_id: UUID,
):
    """
    Activate an RSA key pair.
    """
    key_pair = crud.rsa_key_pair.update_status(db=db, id=key_id, status="active")
    if not key_pair:
        raise HTTPException(status_code=404, detail="RSA key pair not found")
    return {"message": "RSA key pair activated successfully"}

@router.delete("/{key_id}", response_model=RSAKeyPair)
def delete_rsa_key(
    *,
    db: Session = Depends(deps.get_db),
    key_id: UUID,
) -> RSAKeyPair:
    """
    Delete an RSA key pair.
    """
    key_pair = crud.rsa_key_pair.get(db=db, id=key_id)
    if not key_pair:
        raise HTTPException(status_code=404, detail="RSA key pair not found")
    key_pair = crud.rsa_key_pair.remove(db=db, id=key_id)
    return key_pair
