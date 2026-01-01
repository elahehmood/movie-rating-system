from fastapi import APIRouter, Depends, HTTPException

from app.repositories.movie_repository import MovieRepository, get_movie_repository
from app.schemas.schemas import RatingCreate, RatingResponse

router = APIRouter(prefix="/movies")


@router.post("/{movie_id}/ratings", status_code=201)
def create_rating(
    movie_id: int,
    payload: RatingCreate,
    movie_repo: MovieRepository = Depends(get_movie_repository),
):
    rating = movie_repo.add_rating(movie_id=movie_id, score=payload.score)
    if rating is None:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found.")

    return {
        "status": "success",
        "data": RatingResponse.model_validate(rating).model_dump(),
    }
