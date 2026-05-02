

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


def demo_trie(movies: list):

    print("\ndemo: trie operations\n")
  

    trie = Trie()
    for movie in movies:
        trie.insert(movie.title, movie)

    print(f"  total titles inserted : {len(trie):,}")
    test_prefixes = ["The Dark", "Star Wars", "Toy", "Inc"]
    for prefix in test_prefixes:
        results = trie.search_prefix(prefix, max_results=5)
        print(f"\n  Prefix: '{prefix}'  ->  {len(results)} matches (showing up to 5):")
        for m in results[:5]:
            print(f"    - {m.title}  [{', '.join(m.genres)}]  avg_rating={m.avg_rating:.2f}")

    exact_title = "Pulp Fiction (1994)"
    exact_results = trie.search_exact(exact_title)
    print(f"\n  Exact Trie search: '{exact_title}'")
    for m in exact_results:
        print(f"    -> {m}")

    print(f"\n  starts_with('shrek') : {trie.starts_with('shrek')}")
    print(f"  starts_with('zzzzz') : {trie.starts_with('zzzzz')}")


def main():
    movies_path = MOVIES_PATH if os.path.exists(MOVIES_PATH) else "/documents/darllingsilveiradamota/movies.csv"

    if os.path.exists(RATINGS_PATH):
        ratings_path = RATINGS_PATH
    else:
        ratings_path = None
        print("[main] error: ratings.csv not found.")
        print("[main]       Drop the MovieLens 20M ratings.csv next to main.py to include ratings.\n")

    movies = load_movies(movies_path, ratings_path)
