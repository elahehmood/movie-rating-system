from sqlalchemy.orm import Session
from app.models.models import Genre

class GenreRepository:
    def __init__(self, db: Session):
        self.db = db
    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all available genres.
        """
        return db.query(Genre).all()

    @staticmethod
    def get_by_ids(db: Session, genre_ids: list[int]):
        """
        Retrieve multiple genres by their IDs.
        Useful for associating genres with a movie.
        """
        return db.query(Genre).filter(Genre.id.in_(genre_ids)).all()