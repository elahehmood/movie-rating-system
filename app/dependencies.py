# from fastapi import Depends
# from sqlalchemy.orm import Session

# from app.db.database import get_db
# from app.repositories.movie_repository import (
#     MovieRepository,
#     get_movie_repository,
# )
# from app.services.movie_service import MovieService


# def get_movie_service(
#     movie_repo: MovieRepository = Depends(get_movie_repository),
#     db: Session = Depends(get_db),
# ) -> MovieService:
#     """
#     Dependency function برای تزریق MovieService.

#     DirectorRepository و GenreRepository static هستند،
#     پس db مستقیم به Service داده می‌شود.
#     """
#     service = MovieService(
#         movie_repo=movie_repo,
#         director_repo=None,
#         genre_repo=None,
#     )
#     service.db = db  # تزریق session برای static repoها
#     return service
# app/dependencies/service_dependencies.py
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
