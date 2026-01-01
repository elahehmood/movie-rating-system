from typing import Optional, Dict, Any
from fastapi import Depends

from app.repositories.movie_repository import MovieRepository, get_movie_repository
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
class MovieService:
    
    
    def __init__(
        self,
        movie_repo: MovieRepository,
        director_repo: DirectorRepository,
        genre_repo: GenreRepository
    ):
        self.movie_repo = movie_repo
        self.director_repo = director_repo
        self.genre_repo = genre_repo
        

    
    # def get_movies_list(
    #     self,
    #     page: int = 1,
    #     page_size: int = 10,
    #     title: Optional[str] = None,
    #     release_year: Optional[int] = None,
    #     genre_name: Optional[str] = None
    # ) -> Dict[str, Any]:
    #     """
    #     Get paginated list of movies.
    #     """
    #     skip = (page - 1) * page_size
        
    #     movies = self.movie_repo.get_all(
    #         skip=skip,
    #         limit=page_size,
    #         title=title,
    #         release_year=release_year,
    #         genre_name=genre_name
    #     )
        
    #     total_items = self.movie_repo.get_total_count(
    #         title=title,
    #         release_year=release_year,
    #         genre_name=genre_name
    #     )
        
    #     items = []
    #     for movie in movies:
    #         ratings = movie.ratings
    #         avg_rating = round(sum(r.score for r in ratings) / len(ratings), 1) if ratings else None
            
    #         items.append({
    #             "id": movie.id,
    #             "title": movie.title,
    #             "release_year": movie.release_year,
    #             "director": {
    #                 "id": movie.director.id,
    #                 "name": movie.director.name
    #             },
    #             "genres": [genre.name for genre in movie.genres],
    #             "average_rating": avg_rating,
    #             "ratings_count": len(ratings)
    #         })
        
    #     return {
    #         "page": page,
    #         "page_size": page_size,
    #         "total_items": total_items,
    #         "items": items
    #     }
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific movie.
        """
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            return None
        
        ratings = movie.ratings
        avg_rating = round(sum(r.score for r in ratings) / len(ratings), 1) if ratings else None
        
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {
                "id": movie.director.id,
                "name": movie.director.name
            },
            "genres": [genre.name for genre in movie.genres],
            "cast": movie.cast,
            "average_rating": avg_rating,
            "ratings_count": len(ratings)
        }
    
    def create_movie(
        self,
        title: str,
        director_id: int,
        release_year: int,
        cast: list[str],
        genre_ids: list[int]
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new movie with validation.
        """
        if not self.movie_repo.director_exists(director_id):
            return None
        
        if not self.movie_repo.genres_exist(genre_ids):
            return None
        
        created_movie = self.movie_repo.create(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast,
            genre_ids=genre_ids
        )
        
        return {
            "id": created_movie.id,
            "title": created_movie.title,
            "release_year": created_movie.release_year,
            "director": {
                "id": created_movie.director.id,
                "name": created_movie.director.name
            },
            "genres": [genre.name for genre in created_movie.genres],
            "cast": created_movie.cast,
            "average_rating": None,
            "ratings_count": 0
        }
    @staticmethod
    def update_movie(
        repository: MovieRepository,
        movie_id: int,
        movie_data: dict
    ) -> Optional[Dict]:
        """
        به‌روزرسانی فیلم موجود
        """
        try:
            # بررسی وجود director_id (اگر ارسال شده)
            if 'director_id' in movie_data and movie_data['director_id']:
                if not repository.director_exists(movie_data['director_id']):
                    return None
            
            # بررسی وجود ژانرها (اگر ارسال شده)
            if 'genres' in movie_data and movie_data['genres']:
                if not repository.genres_exist(movie_data['genres']):
                    return None
            
            # آپدیت فیلم
            updated_movie = repository.update(
                movie_id=movie_id,
                title=movie_data.get('title'),
                director_id=movie_data.get('director_id'),
                release_year=movie_data.get('release_year'),
                cast=movie_data.get('cast'),
                genre_ids=movie_data.get('genres')
            )
            
            if not updated_movie:
                return None
            
            # ساخت پاسخ
            genre_names = [mg.genre.name for mg in updated_movie.movie_genres]
            
            # محاسبه آمار ratings
            ratings = updated_movie.ratings
            avg_rating = sum(r.score for r in ratings) / len(ratings) if ratings else None
            
            return {
                "id": updated_movie.id,
                "title": updated_movie.title,
                "release_year": updated_movie.release_year,
                "director": {
                    "id": updated_movie.director.id,
                    "name": updated_movie.director.name
                },
                "genres": genre_names,
                "cast": updated_movie.cast,
                "average_rating": round(avg_rating, 1) if avg_rating else None,
                "ratings_count": len(ratings)
            }
            
        except Exception as e:
            print(f"Service error in update_movie: {e}")
            return None
    def delete_movie(self, movie_id: int) -> bool:
        """
        حذف فیلم - True یا False برمی‌گردونه
        """
        return self.movie_repo.delete(movie_id)


# # ✅ این تابع در Service تعریف میشه تا Controller بتونه ازش استفاده کنه
# def get_movie_service(
#     repository: MovieRepository = Depends(get_movie_repository)
# ) -> MovieService:
#     """
#     Dependency function برای تزریق Service.
#     این تابع Repository رو میگیره و Service رو می‌سازه.
#     """
#     return MovieService(repository)




