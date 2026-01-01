from typing import Optional, Dict, Any, Tuple, List

from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.schemas.schemas import MovieResponse, DirectorInMovieResponse


class MovieService:
    """Business logic layer (Service).
    Controller calls Service; Service talks to repositories.
    """

    def __init__(
        self,
        movie_repo: MovieRepository,
        director_repo: DirectorRepository,
        genre_repo: GenreRepository,
    ):
        self.movie_repo = movie_repo
        self.director_repo = director_repo
        self.genre_repo = genre_repo

    # ----------------------------
    # Helpers (business logic)
    # ----------------------------
    def _calc_rating_stats(self, movie) -> Tuple[Optional[float], int]:
        ratings = getattr(movie, "ratings", []) or []
        scores = [r.score for r in ratings if r is not None and getattr(r, "score", None) is not None]
        if not scores:
            return None, 0
        return sum(scores) / len(scores), len(scores)

    def _movie_to_response(self, movie) -> MovieResponse:
        avg, cnt = self._calc_rating_stats(movie)
        return MovieResponse(
            id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            cast=movie.cast or "",
            director=DirectorInMovieResponse.model_validate(movie.director),
            genres=[g.name for g in getattr(movie, "genres", [])],
            average_rating=avg,
            ratings_count=cnt,
        )

    # ----------------------------
    # Use-cases
    # ----------------------------
    def get_movies_list(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated list of movies with optional filters."""
        skip = (page - 1) * page_size

        movies = self.movie_repo.get_all(
            skip=skip,
            limit=page_size,
            title=title,
            release_year=release_year,
            genre_name=genre_name,
        )

        total_items = self.movie_repo.get_total_count(
            title=title,
            release_year=release_year,
            genre_name=genre_name,
        )

        return {
            "status": "success",
            "data": {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "items": [self._movie_to_response(m).model_dump() for m in movies],
            },
        }

    def get_movie_by_id(self, movie_id: int) -> Optional[MovieResponse]:
        """Get detailed information about a specific movie."""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            return None
        return self._movie_to_response(movie)

    def create_movie(
        self,
        title: str,
        director_id: int,
        release_year: int,
        cast: str,
        genre_ids: List[int],
    ) -> Optional[MovieResponse]:
        """Create a new movie with validation."""
        if not self.movie_repo.director_exists(director_id):
            return None

        if not self.movie_repo.genres_exist(genre_ids):
            return None

        created_movie = self.movie_repo.create(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast,
            genre_ids=genre_ids,
        )

        return self._movie_to_response(created_movie)

    def update_movie(self, movie_id: int, movie_data: dict) -> Optional[MovieResponse]:
        """Update an existing movie."""
        if "director_id" in movie_data and movie_data["director_id"]:
            if not self.movie_repo.director_exists(movie_data["director_id"]):
                return None

        if "genres" in movie_data and movie_data["genres"]:
            if not self.movie_repo.genres_exist(movie_data["genres"]):
                return None

        updated_movie = self.movie_repo.update(
            movie_id=movie_id,
            title=movie_data.get("title"),
            director_id=movie_data.get("director_id"),
            release_year=movie_data.get("release_year"),
            cast=movie_data.get("cast"),
            genre_ids=movie_data.get("genres"),
        )

        if not updated_movie:
            return None

        return self._movie_to_response(updated_movie)

    def delete_movie(self, movie_id: int) -> bool:
        """Delete a movie."""
        return self.movie_repo.delete(movie_id)
