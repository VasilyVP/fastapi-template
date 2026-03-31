from fastapi import APIRouter

from app.api.v1.endpoints import auth, items, system, users


api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(items.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
