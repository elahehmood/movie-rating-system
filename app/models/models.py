from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

# --- Association Table for Many-to-Many relationship (Movies <-> Genres) ---
# Defined in the docs as 'movie_genres' with a composite primary key.
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

# --- Director Model ---
class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    # Relationship: One Director -> Many Movies
    movies = relationship("Movie", back_populates="director")

# --- Genre Model ---
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationship: Many Genres <-> Many Movies (via Association Table)
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

# --- Movie Model ---
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    release_year = Column(Integer, nullable=False)
    cast = Column(String, nullable=True)  # Stores actor names as a string
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)

    # Relationships
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    
    # Relationship: One Movie -> Many Ratings
    # cascade="all, delete" ensures ratings are deleted if the movie is deleted
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

# --- Rating Model ---
class Rating(Base):
    __tablename__ = "movie_ratings"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)  # Business logic will validate 1-10 range
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    # Relationship to Movie
    movie = relationship("Movie", back_populates="ratings")