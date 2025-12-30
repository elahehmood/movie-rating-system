from pydantic import BaseModel
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
    cast: Optional[str] = None

class MovieCreate(MovieBase):
    director_id: int
    genre_ids: List[int] = []

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None

class MovieResponse(MovieBase):
    id: int
    director: Optional[DirectorResponse] = None
    genres: List[GenreResponse] = []
    ratings: List[RatingResponse] = []
    
    class Config:
        from_attributes = True