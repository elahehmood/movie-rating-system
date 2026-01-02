from sqlalchemy.orm import Session
from app.models.models import Rating

class RatingRepository:
    def __init__(self, db: Session):
        self.db = db
    @staticmethod
    def create(db: Session, rating: Rating):
        """
        Add a new rating to the database.
        """
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating