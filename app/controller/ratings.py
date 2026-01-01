from fastapi import APIRouter, Depends, HTTPException, Path

from app.repositories.movie_repository import MovieRepository, get_movie_repository
from app.schemas.schemas import RatingCreate

router = APIRouter(prefix="/movies", tags=["ratings"])


@router.post("/{movie_id}/ratings")
def create_rating(
    movie_id: int = Path(..., gt=0),
    payload: RatingCreate = ...,
    movie_repo: MovieRepository = Depends(get_movie_repository),
):
    if payload.score < 1 or payload.score > 10:
        raise HTTPException(status_code=422, detail={"code": 422, "message": "score must be between 1 and 10"})

    rating = movie_repo.add_rating(movie_id=movie_id, score=payload.score)
    if rating is None:
        raise HTTPException(status_code=404, detail={"code": 404, "message": "Movie not found"})

    return {"status": "success", "data": {"id": rating.id, "movie_id": rating.movie_id, "score": rating.score}}
