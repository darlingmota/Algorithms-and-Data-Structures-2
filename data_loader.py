
# Loads the MovieLens CSV files into Movie objects.


import csv
import os
from models import Movie


# Loads movies.csv and  aggregates rating stats from ratings.csv
def load_movies(movies_path: str, ratings_path: str = None) -> list:

    # stream the ratings file and build up totals per movie
    rating_totals = {}   

    if ratings_path and os.path.exists(ratings_path):
        file_size_mb = os.path.getsize(ratings_path) / (1024 * 1024)
        print(f"[DataLoader] Streaming ratings from: {ratings_path}")
        print(f"[DataLoader] File size: {file_size_mb:.1f} MB - row-by-row streaming...")

