from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.dependencies import get_movie_service
from app.schemas.schemas import MovieCreate, MovieResponse, MovieCreateResponse, MovieUpdate
from app.services.movie_service import MovieService

router = APIRouter()


@router.get("/movies/", summary="List movies (filter & pagination)")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None),
    genre: Optional[str] = Query(None),
    service: MovieService = Depends(get_movie_service),
):
    """
    Get paginated list of movies with optional filters.
    """
    return service.get_movies_list(
        page=page,
        page_size=page_size,
        title=title,
        release_year=release_year,
        genre_name=genre,
    )


@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(
    movie_id: int,
    service: MovieService = Depends(get_movie_service)
):
    """
    Get details of a specific movie by ID.
    """
    movie = service.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id {movie_id} not found"
        )
    return movie


@router.post("/movies/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_data: MovieCreate,
    service: MovieService = Depends(get_movie_service)
):
    """
    Create a new movie.
    Validates director_id and genre IDs before creation.
    """
    created_movie = service.create_movie(
        title=movie_data.title,
        director_id=movie_data.director_id,
        release_year=movie_data.release_year,
        cast=movie_data.cast,
        genre_ids=movie_data.genres
    )

    if not created_movie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid director_id or genre_ids"
        )

    return created_movie


@router.put("/movies/{movie_id}/", response_model=MovieCreateResponse)
async def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    service: MovieService = Depends(get_movie_service)
):
    """
    به‌روزرسانی اطلاعات یک فیلم موجود
    """
    try:
        movie_data = movie.model_dump(exclude_unset=True)
        result = service.update_movie(movie_id, movie_data)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "failure",
                    "error": {
                        "code": 404,
                        "message": "Movie not found"
                    }
                }
            )

        return MovieCreateResponse(status="success", data=result)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Controller error: {e}")
        raise HTTPException(
            status_code=422,
            detail={
                "status": "failure",
                "error": {
                    "code": 422,
                    "message": "Invalid director_id or genres"
                }
            }
        )


@router.delete(
    "/movies/{movie_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a movie"
)
def delete_movie(
    movie_id: int,
    service: MovieService = Depends(get_movie_service)
):
    """
    حذف یک فیلم به همراه تمام رکوردهای وابسته
    """
    deleted = service.delete_movie(movie_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "failure",
                "error": {
                    "code": 404,
                    "message": "Movie not found"
                }
            }
        )
