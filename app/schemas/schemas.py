from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# --- Genre Schemas ---
class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreResponse(GenreBase):
    id: int
    class Config:
        from_attributes = True

# --- Director Schemas ---
class DirectorBase(BaseModel):
    name: str
    birth_year: Optional[int] = None
    description: Optional[str] = None

class DirectorResponse(DirectorBase):
    id: int
    class Config:
        from_attributes = True

# ✅ Director ساده برای Movie Response
class DirectorInMovieResponse(BaseModel):
    """Schema برای نمایش کارگردان در پاسخ فیلم"""
    id: int
    name: str
    class Config:
        from_attributes = True

# --- Rating Schemas ---
class RatingCreate(BaseModel):
    score: int 
    # = Field(..., ge=1, le=10)
class RatingResponse(RatingCreate):
    id: int
    movie_id: int
    class Config:
        from_attributes = True

# --- Movie Schemas ---
class MovieBase(BaseModel):
    title: str
    release_year: int
    cast: str = Field(..., min_length=1)

# ✅ Schema برای ایجاد فیلم (POST)
class MovieCreate(MovieBase):
    director_id: int = Field(..., gt=0)
    genres: List[int] = Field(..., min_items=1)
    release_year: int= Field(...,ge=1500,le=2030)
    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Godfather",
                "director_id": 3,
                "release_year": 1972,
                "cast": "Marlon Brando",
                "genres": [1, 2]
            }
        }

# ✅ Schema برای آپدیت فیلم
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    director_id: Optional[int] = None
    genres: Optional[List[int]] = None

# ✅ Schema برای پاسخ جزئیات فیلم (GET)
class MovieResponse(MovieBase):
    id: int
    director: DirectorInMovieResponse
    genres: List[str]
    average_rating: Optional[float] = None
    ratings_count: int = 0

    class Config:
        from_attributes = True

# ✅ Schema برای پاسخ موفق
class MovieCreateResponse(BaseModel):
    status: str = "success"
    data: MovieResponse

# ✅ Schema برای پاسخ خطا
class ErrorResponse(BaseModel):
    status: str = "failure"
    error: dict

    class Config:
        json_schema_extra = {
            "example": {
                "status": "failure",
                "error": {
                    "code": 422,
                    "message": "Invalid director_id or genres"
                }
            }
        }
