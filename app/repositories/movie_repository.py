from sqlalchemy.orm import Session, joinedload
from app.models.models import Movie, Genre

class MovieRepository:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10, title: str = None, release_year: int = None, genre_name: str = None):
        """
        Retrieve a list of movies with optional filtering by title, year, or genre.
        Includes eager loading for Director and Genres relationships.
        """
        # Start query with eager loading to prevent N+1 query problems
        query = db.query(Movie).options(joinedload(Movie.director), joinedload(Movie.genres))
        
        # Apply filters based on provided arguments
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre_name:
            # Join with genres table to filter by genre name
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, movie_id: int):
        """
        Retrieve a single movie by ID, including its director, genres, and ratings.
        """
        return db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
            joinedload(Movie.ratings)
        ).filter(Movie.id == movie_id).first()

    @staticmethod
    def create(db: Session, movie: Movie, genre_ids: list[int]):
        """
        Create a new movie and associate it with existing genres.
        """
        if genre_ids:
            # Fetch genre objects by their IDs
            genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            movie.genres = genres
        
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie

    @staticmethod
    def delete(db: Session, movie_id: int):
        """
        Delete a movie by ID. Returns True if deleted, False if not found.
        """
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            db.delete(movie)
            db.commit()
            return True
        return False