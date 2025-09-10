from fastapi import APIRouter
from app.api.api_v1.endpoints import tenants, sites, rsa_keys

api_router = APIRouter()
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(rsa_keys.router, prefix="/keys", tags=["rsa-keys"])
