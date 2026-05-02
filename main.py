

import os
import random

from data_loader import load_movies
from hash_map import HashMap
from trie import Trie
from benchmark import (
    benchmark_insertion,
    benchmark_exact_search,
    benchmark_prefix_search,
    benchmark_trie_vs_hashmap_exact,
    benchmark_memory_usage,
    print_summary,
    DATASET_SIZES,
)



MOVIES_PATH = "movies.csv"
RATINGS_PATH = "ratings.csv"   # the MovieLens 20M ratings file
