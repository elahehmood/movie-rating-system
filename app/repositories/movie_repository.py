from sqlalchemy.orm import Session, joinedload
from fastapi import Depends

from app.models.models import Movie, Genre, Director, movie_genres, Rating
from app.db.database import get_db
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy import delete

class MovieRepository:
    
    def __init__(self, db: Session):
        """
        Repository تنها لایه‌ای است که با Session کار می‌کنه.
        """
        self.db = db
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        title: str = None,
        release_year: int = None,
        genre_name: str = None
    ):
        """
        Retrieve movies from database with filters.
        """
        query = self.db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
            joinedload(Movie.ratings)
        )
        
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, movie_id: int):
        """
        Retrieve a single movie by ID.
        """
        return self.db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
            joinedload(Movie.ratings)
        ).filter(Movie.id == movie_id).first()
    
    def create(
        self,
        title: str,
        director_id: int,
        release_year: int,
        cast: list[str],
        genre_ids: list[int] = None
    ):
        """
        Create a new movie.
        """
        new_movie = Movie(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast
        )
        
        if genre_ids:
            genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            new_movie.genres = genres
        
        self.db.add(new_movie)
        self.db.commit()
        self.db.refresh(new_movie)
        
        return new_movie
    
    def director_exists(self, director_id: int) -> bool:
        """
        Check if a director exists.
        """
        return self.db.query(Director).filter(Director.id == director_id).first() is not None
    
    def genres_exist(self, genre_ids: list[int]) -> bool:
        """
        Check if all genres exist.
        """
        found_genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        return len(found_genres) == len(genre_ids)
    
    def get_total_count(
        self,
        title: str = None,
        release_year: int = None,
        genre_name: str = None
    ) -> int:
        """
        Get total count for pagination.
        """
        query = self.db.query(Movie)
        
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))
        
        return query.count()
    def update(
        self, 
        movie_id: int, 
        genre_ids: Optional[List[int]] = None,
        **kwargs
    ) -> Optional[Movie]:
        """آپدیت فیلم"""
        movie = self.get_by_id(movie_id)
        if not movie:
            return None
        
        # آپدیت فیلدهای ساده
        for key, value in kwargs.items():
            if value is not None:
                setattr(movie, key, value)
        
        # آپدیت ژانرها
        if genre_ids is not None:
            new_genres = self.db.query(Genre).filter(
                Genre.id.in_(genre_ids)
            ).all()
            movie.genres = new_genres
        
        self.db.commit()
        self.db.refresh(movie)
        return movie
    def delete(self, movie_id: int) -> bool:
        """
        حذف فیلم - اگر موفق باشه True برمی‌گردونه، وگرنه False
        """
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        
        if not movie:
            return False
        
        # حذف رکوردهای وابسته
        self.db.execute(
            delete(movie_genres).where(movie_genres.c.movie_id == movie_id)
        )
        self.db.query(Rating).filter(Rating.movie_id == movie_id).delete()
        
        # حذف فیلم
        self.db.delete(movie)
        self.db.commit()
        
        return True

# ✅ این تابع در Repository تعریف میشه
def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    """
    Dependency function برای تزریق Repository.
    فقط اینجا Session از Database گرفته میشه!
    """
    return MovieRepository(db)



