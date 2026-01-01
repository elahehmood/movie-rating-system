from app.db.database import SessionLocal
from app.models.models import Genre, Director, Movie

def seed_data():
    db = SessionLocal()
    print("🌱 Seeding data...")

    # 1. Add Genres
    genres_data = ["Action", "Drama", "Sci-Fi", "Comedy", "Horror"]
    db_genres = []
    
    # Check if genres exist to avoid duplication
    if db.query(Genre).count() == 0:
        for name in genres_data:
            # Added description as per your model
            genre = Genre(name=name, description=f"Movies belonging to {name} category")
            db.add(genre)
            db_genres.append(genre)
        print("   ✅ Genres added.")
    else:
        print("   ⚠️ Genres already exist. Skipping.")
        db_genres = db.query(Genre).all()
    
    # Commit to generate IDs
    db.commit()

    # 2. Add Directors (including birth_year)
    directors_data = [
        {"name": "Christopher Nolan", "birth_year": 1970},
        {"name": "Quentin Tarantino", "birth_year": 1963},
        {"name": "Martin Scorsese", "birth_year": 1942}
    ]
    
    db_directors = []
    if db.query(Director).count() == 0:
        for d in directors_data:
            director = Director(name=d["name"], birth_year=d["birth_year"])
            db.add(director)
            db_directors.append(director)
        print("   ✅ Directors added.")
    else:
        print("   ⚠️ Directors already exist. Skipping.")
        db_directors = db.query(Director).all()

    db.commit()

    # 3. Add a Sample Movie (Optional)
    # Only adds a movie if none exist and we have dependencies
    if db.query(Movie).count() == 0 and db_directors and db_genres:
        nolan = db_directors[0] # Selecting Christopher Nolan
        action_genre = db_genres[0] # Selecting Action
        
        # Creating movie with 'cast' field
        movie = Movie(
            title="Inception",
            release_year=2010,
            cast="Leonardo DiCaprio, Joseph Gordon-Levitt", 
            director_id=nolan.id
        )
        # Associate genre
        movie.genres.append(action_genre)
        
        db.add(movie)
        db.commit()
        print("   ✅ Sample movie 'Inception' added.")

    db.close()
    print("🏁 Seeding process finished!")

if __name__ == "__main__":
    seed_data()

