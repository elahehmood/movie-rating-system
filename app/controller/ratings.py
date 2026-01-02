from app.core.logger import get_logger

logger = get_logger("movie_rating")

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.movie_repository import MovieRepository, get_movie_repository
from app.schemas.schemas import RatingCreate, RatingResponse

router = APIRouter(prefix="/movies")


# @router.post("/{movie_id}/ratings", status_code=201)
# def create_rating(
#     movie_id: int,
#     payload: RatingCreate,
#     movie_repo: MovieRepository = Depends(get_movie_repository),
# ):
#     rating = movie_repo.add_rating(movie_id=movie_id, score=payload.score)
#     if rating is None:
#         raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found.")

#     return {
#         "status": "success",
#         "data": RatingResponse.model_validate(rating).model_dump(),
#     }
@router.post("/{movie_id}/ratings", status_code=201)
def create_rating(
    movie_id: int,
    payload: RatingCreate,
    movie_repo: MovieRepository = Depends(get_movie_repository),
):
    route = f"/api/v1/movies/{movie_id}/ratings"

    # ✅ INFO — شروع ثبت امتیاز
    logger.info(
        "Rating movie "
        f"(movie_id={movie_id}, rating={payload.score}, route={route})"
    )

    # ✅ WARNING — امتیاز نامعتبر
    if payload.score < 1 or payload.score > 10:
        logger.warning(
            "Invalid rating value "
            f"(movie_id={movie_id}, rating={payload.score}, route={route})"
        )
        raise HTTPException(status_code=400, detail="Invalid rating value")

    try:
        rating = movie_repo.add_rating(movie_id=movie_id, score=payload.score)

        if rating is None:
            raise HTTPException(
                status_code=404,
                detail=f"Movie with id {movie_id} not found."
            )

        # ✅ INFO — موفق
        logger.info(
            "Rating saved successfully "
            f"(movie_id={movie_id}, rating={payload.score})"
        )

        return {
            "status": "success",
            "data": RatingResponse.model_validate(rating).model_dump(),
        }

    except HTTPException:
        raise

    except Exception:
        # ✅ ERROR — خطای سیستمی
        logger.error(
            "Failed to save rating "
            f"(movie_id={movie_id}, rating={payload.score})",
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal server error")
