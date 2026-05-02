
# Loads the dataset, runs quick demos to show the structures work, then runs all the benchmarks.


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


# show the structures actually working before benchmarking

def demo_hashmap(movies: list):
    
    print("demo - hashmap operations")
    

    hm = HashMap()

    # insert each movie twice.  once by title, once by ID, both keys point to the same Movie
    for movie in movies:
        hm.insert(movie.title.lower(), movie)
        hm.insert(movie.movie_id, movie)

    print(f"  Total entries  : {len(hm):,}  (titles + IDs = {len(movies)*2:,})")

    # try an exact title search
    test_title = "Toy Story (1995)"
    result = hm.search(test_title.lower())
    print(f"\n  Search by title: '{test_title}'")
    print(f"  Result         : {result}")

    # try an exact ID search
    test_id = 1
    result_id = hm.search(test_id)
    print(f"\n  Search by ID   : {test_id}")
    print(f"  Result         : {result_id}")

    # try something that doesn't exist
    missing = hm.search("this movie does not exist")
    print(f"\n  Missing key    : 'this movie does not exist'")
    print(f"  Result         : {missing}")

    # collision diagnostics so I can show the hash function isn't terrible
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

    # try a few prefix searches to show autocomplete works
    test_prefixes = ["The Dark", "Star Wars", "Toy", "Inc"]
    for prefix in test_prefixes:
        results = trie.search_prefix(prefix, max_results=5)
        print(f"\n  Prefix: '{prefix}'  ->  {len(results)} matches (showing up to 5):")
        for m in results[:5]:
            print(f"    - {m.title}  [{', '.join(m.genres)}]  avg_rating={m.avg_rating:.2f}")

    # exact search via the Trie too
    exact_title = "Pulp Fiction (1994)"
    exact_results = trie.search_exact(exact_title)
    print(f"\n  Exact Trie search: '{exact_title}'")
    for m in exact_results:
        print(f"    -> {m}")

    # quick starts_with checks
    print(f"\n  starts_with('shrek') : {trie.starts_with('shrek')}")
    print(f"  starts_with('zzzzz') : {trie.starts_with('zzzzz')}")


# main

def main():
    
    # try local file first fall back to the upload path if running on the sandbox
    movies_path = MOVIES_PATH if os.path.exists(MOVIES_PATH) else "/documents/darllingsilveiradamota/movies.csv"

    if os.path.exists(RATINGS_PATH):
        ratings_path = RATINGS_PATH
    else:
        ratings_path = None
        print("[main] error: ratings.csv not found.")
        print("[main]       Drop the MovieLens 20M ratings.csv next to main.py to include ratings.\n")

    movies = load_movies(movies_path, ratings_path)

    # fix the random seed so the benchmarks are reproducible
    random.seed(42)

    # demos first, so I know everything works before running the long benchmarks
    demo_hashmap(movies)
    demo_trie(movies)

    # all the benchmarks
    insertion_results = benchmark_insertion(movies)
    exact_results = benchmark_exact_search(movies)
    prefix_results = benchmark_prefix_search(movies)
    trie_vs_hm_results = benchmark_trie_vs_hashmap_exact(movies)
    memory_results = benchmark_memory_usage(movies, DATASET_SIZES)

    # summary
    print_summary(insertion_results, exact_results, prefix_results, trie_vs_hm_results)

    # summary table
   
    print("\nmemory usage summary\n")

    print(f"\n{'Size':<8} {'HashMap (MB)':>14} {'Trie (MB)':>14} {'Trie/HM':>10} "
          f"{'HM (KB/item)':>14} {'Trie (KB/item)':>16}")
    print("-" * 80)
    for size, mem in memory_results.items():
        ratio = mem['trie_memory_mb'] / mem['hashmap_memory_mb'] if mem['hashmap_memory_mb'] > 0 else 0
        print(f"{size:<8} {mem['hashmap_memory_mb']:14.2f} {mem['trie_memory_mb']:14.2f} "
              f"{ratio:9.2f}x {mem['hashmap_per_item_kb']:14.2f} {mem['trie_per_item_kb']:16.2f}")

    print("\nbenchmarks complete.")


if __name__ == "__main__":
    main()