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

# ✅ Director ساده برای Movie Response (طبق سند)
class DirectorInMovieResponse(BaseModel):
    """Schema برای نمایش کارگردان در پاسخ فیلم"""
    id: int
    name: str
    class Config:
        from_attributes = True

# --- Rating Schemas ---
class RatingCreate(BaseModel):
    score: int  # User only sends the score

class RatingResponse(RatingCreate):
    id: int
    movie_id: int
    class Config:
        from_attributes = True

# --- Movie Schemas ---
class MovieBase(BaseModel):
    title: str
    release_year: int
    cast: str = Field(..., min_items=1)  

# ✅ Schema برای ایجاد فیلم (POST)
class MovieCreate(MovieBase):
    director_id: int = Field(..., gt=0)
    genres: List[int] = Field(..., min_items=1)  # ✅ اصلاح نام: genres به جای genre_ids

    # @field_validator('cast')
    # @classmethod
    # def validate_cast(cls, v):
    #     if not all(isinstance(item, str) and len(item.strip()) > 0 for item in v):
    #         raise ValueError("همه بازیگران باید رشته‌های معتبر باشند")
    #     return v

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

# ✅ Schema برای آپدیت فیلم (PATCH - برای Endpoint بعدی)
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None  # ✅ اصلاح شد
    director_id: Optional[int] = None
    genres: Optional[List[int]] = None  # ✅ اصلاح نام

# ✅ Schema برای پاسخ جزئیات فیلم (GET)
class MovieResponse(MovieBase):
    id: int
    director: DirectorInMovieResponse  # ✅ استفاده از schema ساده‌تر
    genres: List[str]  # ✅ فقط نام ژانرها (نه کل object)
    average_rating: Optional[float]  # ✅ اضافه شد
    ratings_count: int  # ✅ اضافه شد
    
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
