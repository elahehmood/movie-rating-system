from fastapi import APIRouter
from app.controller import movies, ratings  

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(movies.router, tags=["movies"])
api_router.include_router(ratings.router, tags=["ratings"])
