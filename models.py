
class Movie:
    def __init__(self, movie_id: int, title: str, genres: str,
                 avg_rating: float = 0.0, rating_count: int = 0):
        self.movie_id = movie_id
        self.title = title
        self.genres = [g.strip() for g in genres.split("|")] if genres else []
        self.avg_rating = avg_rating
        self.rating_count = rating_count
