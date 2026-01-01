from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.services.movie_service import MovieService


def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    """
    ✅ فقط این تابع db می‌بینه
    همه Repository ها رو می‌سازه و به Service تزریق می‌کنه
    """
    # ساخت تمام Repository ها
    movie_repo = MovieRepository(db)
    director_repo = DirectorRepository(db)
    genre_repo = GenreRepository(db)
    
    # ساخت Service با همه Repository ها
    return MovieService(
        movie_repo=movie_repo,
        director_repo=director_repo,
        genre_repo=genre_repo
    )
