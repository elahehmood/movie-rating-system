import logging
from fastapi import HTTPException

from app.repositories.rating_repository import RatingRepository
from app.schemas.schemas import RatingCreateOut

logger = logging.getLogger(__name__)


class RatingsService:
    def __init__(self, repo: RatingRepository) -> None:
        self.repo = repo

    def create_rating(self, *, movie_id: int, score: int):
        if score < 1 or score > 10:
            logger.warning("Invalid score", extra={"movie_id": movie_id, "score": score})
            raise HTTPException(status_code=422, detail="Score must be between 1 and 10.")

        if not self.repo.movie_exists(movie_id):
            raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found.")

        rating = self.repo.create_rating(movie_id=movie_id, score=score)

        out = RatingCreateOut(
            rating_id=rating.id,
            movie_id=rating.movie_id,
            score=rating.score,
            created_at=getattr(rating, "created_at", None),
        )
        return {"status": "success", "data": out.model_dump()}
