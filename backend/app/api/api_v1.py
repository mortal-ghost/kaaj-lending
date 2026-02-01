from fastapi import APIRouter

from app.api.endpoints import applications, lenders

api_router = APIRouter()
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(lenders.router, prefix="/lenders", tags=["lenders"])
