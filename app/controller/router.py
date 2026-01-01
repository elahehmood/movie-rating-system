from fastapi import APIRouter
from app.controller.movies import router as movies_router
from app.controller.ratings import router as ratings_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(movies_router)
api_router.include_router(ratings_router)
