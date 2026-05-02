

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

def demo_hashmap(movies: list):
    
    print("demo - hashmap operations")
    

    hm = HashMap()
    for movie in movies:
        hm.insert(movie.title.lower(), movie)
        hm.insert(movie.movie_id, movie)

    print(f"  Total entries  : {len(hm):,}  (titles + IDs = {len(movies)*2:,})")

    test_title = "Toy Story (1995)"
    result = hm.search(test_title.lower())
    print(f"\n  Search by title: '{test_title}'")
    print(f"  Result         : {result}")

    test_id = 1
    result_id = hm.search(test_id)
    print(f"\n  Search by ID   : {test_id}")
    print(f"  Result         : {result_id}")
    missing = hm.search("this movie does not exist")
    print(f"\n  Missing key    : 'this movie does not exist'")
    print(f"  Result         : {missing}")

    stats = hm.collision_stats()
    print(f"\n  hashmap diagnostics:")
    print(f"    Capacity         : {stats['total_buckets']:,}")
    print(f"    Occupied buckets : {stats['occupied_buckets']:,}")
    print(f"    Load factor      : {stats['load_factor']:.4f}")
    print(f"    Max chain length : {stats['max_chain_length']}")
    print(f"    Avg chain length : {stats['avg_chain_length']:.4f}")

