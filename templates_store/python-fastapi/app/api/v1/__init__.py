"""API v1 router — registers all endpoint groups."""

from fastapi import APIRouter

from app.api.v1.routes import router as routes_router

api_router = APIRouter()

api_router.include_router(routes_router)
