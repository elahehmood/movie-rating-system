from __future__ import annotations

from typing import Optional, List, Tuple, Union

from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.models.models import Movie, Genre, Director, movie_genres, Rating


class MovieRepository:
    """
    Repository is the only layer that talks to SQLAlchemy Session.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre_name: Optional[str] = None,
    ) -> List[Movie]:
        """
        Retrieve movies with optional filtering.
        """
        query = self.db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
            joinedload(Movie.ratings),
        )

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year is not None:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """
        Retrieve one movie by id (with relations).
        """
        return (
            self.db.query(Movie)
            .options(
                joinedload(Movie.director),
                joinedload(Movie.genres),
                joinedload(Movie.ratings),
            )
            .filter(Movie.id == movie_id)
            .first()
        )

    def create(
        self,
        title: str,
        director_id: int,
        release_year: int,
        cast: Union[str, List[str]],
        genre_ids: Optional[List[int]] = None,
    ) -> Movie:
        """
        Create a new movie and associate genres.
        """
        new_movie = Movie(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast,
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

    def genres_exist(self, genre_ids: List[int]) -> bool:
        """
        Check if all genres exist.
        """
        found = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        return len(found) == len(genre_ids)

    def get_total_count(
        self,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre_name: Optional[str] = None,
    ) -> int:
        """
        Total count for pagination (with same filters).
        """
        query = self.db.query(Movie)

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year is not None:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))

        return query.count()

    def update(
        self,
        movie_id: int,
        title: Optional[str] = None,
        director_id: Optional[int] = None,
        release_year: Optional[int] = None,
        cast: Optional[Union[str, List[str]]] = None,
        genre_ids: Optional[List[int]] = None,
    ) -> Optional[Movie]:
        """
        Update movie fields + optionally replace genres.
        """
        movie = self.get_by_id(movie_id)
        if not movie:
            return None

        if title is not None:
            movie.title = title
        if director_id is not None:
            movie.director_id = director_id
        if release_year is not None:
            movie.release_year = release_year
        if cast is not None:
            movie.cast = cast

        if genre_ids is not None:
            new_genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            movie.genres = new_genres

        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie_id: int) -> bool:
        """
        Delete movie and dependent records.
        """
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return False

        # remove relations in association table
        self.db.execute(delete(movie_genres).where(movie_genres.c.movie_id == movie_id))

        # delete ratings
        self.db.query(Rating).filter(Rating.movie_id == movie_id).delete()

        # delete movie
        self.db.delete(movie)
        self.db.commit()
        return True

    def add_rating(self, movie_id: int, score: int) -> Optional[Rating]:
        """
        Add a rating for a movie. Returns None if movie not found.
        """
        movie = self.get_by_id(movie_id)
        if not movie:
            return None

        rating = Rating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    @staticmethod
    def calc_rating_stats(movie: Movie) -> Tuple[Optional[float], int]:
        """
        Calculate average rating and count from loaded ratings relation.
        """
        ratings = getattr(movie, "ratings", None) or []
        scores = [r.score for r in ratings if r is not None and getattr(r, "score", None) is not None]
        count = len(scores)
        if count == 0:
            return None, 0
        return sum(scores) / count, count


def get_movie_repository(db: Session = Depends(get_db)) -> MovieRepository:
    """
    Dependency provider for MovieRepository.
    """
    return MovieRepository(db)
