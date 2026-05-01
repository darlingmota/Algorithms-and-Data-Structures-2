
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

        rows_processed = 0
        with open(ratings_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header line: userId,movieId,rating,timestamp
            for row in reader:
                mid = int(row[1])
                rating = float(row[2])
                if mid not in rating_totals:
                    rating_totals[mid] = [0.0, 0]
                rating_totals[mid][0] += rating
                rating_totals[mid][1] += 1
                rows_processed += 1
                # print a progress update every 2 million rows so I know it's still alive
                if rows_processed % 2_000_000 == 0:
                    print(f"[DataLoader]   ... {rows_processed:,} ratings processed")

        print(f"[DataLoader] Done. {rows_processed:,} ratings across "
              f"{len(rating_totals):,} unique movies.\n")
    else:
        if ratings_path:
            print(f"[DataLoader] error: ratings file not found at '{ratings_path}'")
            print(f"[DataLoader] Continuing without rating data.\n")

