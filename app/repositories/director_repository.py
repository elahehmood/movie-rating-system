from sqlalchemy.orm import Session
from app.models.models import Director

class DirectorRepository:
    @staticmethod
    def get_by_id(db: Session, director_id: int):
        """
        Retrieve a director by ID.
        """
        return db.query(Director).filter(Director.id == director_id).first()
    
    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all directors.
        """
        return db.query(Director).all()