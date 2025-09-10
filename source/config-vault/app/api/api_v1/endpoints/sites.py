from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.api import deps
from app.schemas.site import Site, SiteCreate, SiteUpdate

router = APIRouter()

@router.post("/", response_model=Site)
def create_site(
    *,
    db: Session = Depends(deps.get_db),
    site_in: SiteCreate,
) -> Site:
    """
    Create new site.
    """
    # Verify tenant exists
    tenant = crud.tenant.get(db=db, id=site_in.tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=400,
            detail="The tenant with this ID does not exist in the system.",
        )
    
    # Check if domain already exists
    site = crud.site.get_by_domain(db, domain=site_in.domain)
    if site:
        raise HTTPException(
            status_code=400,
            detail="A site with this domain already exists in the system.",
        )
    
    site = crud.site.create(db=db, obj_in=site_in)
    return site

@router.get("/", response_model=List[Site])
def read_sites(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Site]:
    """
    Retrieve sites.
    """
    sites = crud.site.get_multi(db, skip=skip, limit=limit)
    return sites

@router.get("/{site_id}", response_model=Site)
def read_site(
    *,
    db: Session = Depends(deps.get_db),
    site_id: UUID,
) -> Site:
    """
    Get site by ID.
    """
    site = crud.site.get(db=db, id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.put("/{site_id}", response_model=Site)
def update_site(
    *,
    db: Session = Depends(deps.get_db),
    site_id: UUID,
    site_in: SiteUpdate,
) -> Site:
    """
    Update a site.
    """
    site = crud.site.get(db=db, id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check if new domain already exists
    if site_in.domain:
        existing_site = crud.site.get_by_domain(db, domain=site_in.domain)
        if existing_site and existing_site.id != site_id:
            raise HTTPException(
                status_code=400,
                detail="A site with this domain already exists in the system.",
            )
    
    site = crud.site.update(db=db, db_obj=site, obj_in=site_in)
    return site

@router.delete("/{site_id}", response_model=Site)
def delete_site(
    *,
    db: Session = Depends(deps.get_db),
    site_id: UUID,
) -> Site:
    """
    Delete a site.
    """
    site = crud.site.get(db=db, id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    site = crud.site.remove(db=db, id=site_id)
    return site
