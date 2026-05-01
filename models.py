
class Movie:
    def __init__(self, movie_id: int, title: str, genres: str,
                 avg_rating: float = 0.0, rating_count: int = 0):
        self.movie_id = movie_id
        self.title = title
