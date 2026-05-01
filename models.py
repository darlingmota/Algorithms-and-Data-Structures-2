# models.py
# Movie class - just a container for the fields from the MovieLens CSV

class Movie:
    def __init__(self, movie_id: int, title: str, genres: str,
                 avg_rating: float = 0.0, rating_count: int = 0):
        self.movie_id = movie_id
        self.title = title
        # genres come in as one string separated by | so split them into a list
        self.genres = [g.strip() for g in genres.split("|")] if genres else []
        self.avg_rating = avg_rating
        self.rating_count = rating_count

    def __repr__(self):
        # nicer printout when I want to inspect a Movie object in demos
        genres_str = ", ".join(self.genres) if self.genres else "N/A"
        return (
            f"Movie(id={self.movie_id}, title='{self.title}', "
            f"genres=[{genres_str}], avg_rating={self.avg_rating:.2f}, "
            f"ratings={self.rating_count})"
        )