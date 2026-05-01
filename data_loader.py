
# Loads the MovieLens CSV files into Movie objects.


import csv
import os
from models import Movie


# Loads movies.csv and  aggregates rating stats from ratings.csv
def load_movies(movies_path: str, ratings_path: str = None) -> list:

