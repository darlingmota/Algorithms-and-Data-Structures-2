
# All the experimental benchmarks live here.

# Each timed experiment is repeated trials times and averaged.

import time
import random
import tracemalloc

from hash_map import HashMap
from trie import Trie


# How many times each timing test is repeated to smooth out noise
TRIALS = 5

# max dataset sizing 

DATASET_SIZES = [500, 1000, 2000, 5000, 10000, 20000, 27278]

# prefix queries used for the prefix benchmarks
PREFIX_QUERIES = ["the", "star", "da", "a", "love", "man", "night", "dark", "war", "inc"]

# how many random titles  to look up per exact search test
EXACT_QUERY_COUNT = 20



# runs trials times and returns the average time in seconds
def _average_time(func, trials: int = TRIALS) -> float:
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)



# brute force exact title search through a plain list
def linear_exact_search(movies: list, title: str):
    target = title.lower()
    for movie in movies:
        if movie.title.lower() == target:
            return movie
    return None


def linear_exact_search_by_id(movies: list, movie_id: int):
    for movie in movies:
        if movie.movie_id == movie_id:
            return movie
    return None


def linear_prefix_search(movies: list, prefix: str) -> list:
    prefix_lower = prefix.lower()
    return [m for m in movies if m.title.lower().startswith(prefix_lower)]


def benchmark_insertion(movies: list) -> dict:
    
    print("benchmark 1 - insertion time")
    print(f"  trials per measurement: {TRIALS}")
    print("  theoretical: hashmap O(1) avg per insert, trie O(k) where k=title length")
    

    header = f"{'Size':<10} {'HashMap (s)':<22} {'Trie (s)':<22}"
    print(header)

    results = {}

    for size in DATASET_SIZES:
        subset = movies[:size]

        def do_hashmap_insert():
            hm = HashMap()
            for movie in subset:
                hm.insert(movie.title.lower(), movie)
                hm.insert(movie.movie_id, movie)

        def do_trie_insert():
            trie = Trie()
            for movie in subset:
                trie.insert(movie.title, movie)

        hm_time = _average_time(do_hashmap_insert)
        trie_time = _average_time(do_trie_insert)

        results[size] = {
            "hashmap_insert": hm_time,
            "trie_insert": trie_time,
        }

        print(f"{size:<10} {hm_time:<22.6f} {trie_time:<22.6f}")

    return results


def benchmark_exact_search(movies: list) -> dict:

    print("benchmark 2 - exact search time")
    print(f"  trials per measurement: {TRIALS}")
    print("  theoretical: hashmap O(1) avg, linear scan O(n)")
   

    header = (
        f"{'Size':<10} {'HM Title (s)':<18} "
        f"{'HM ID (s)':<16} {'Lin Title (s)':<18} {'Lin ID (s)':<16}"
    )
    print(header)
    

    results = {}

    for size in DATASET_SIZES:
        subset = movies[:size]

        hm = HashMap()
        for movie in subset:
            hm.insert(movie.title.lower(), movie)
            hm.insert(movie.movie_id, movie)

        sample = random.sample(subset, min(EXACT_QUERY_COUNT, len(subset)))
        titles = [m.title for m in sample]
        ids = [m.movie_id for m in sample]
        def do_hm_title_search():
            for title in titles:
                hm.search(title.lower())

        def do_hm_id_search():
            for mid in ids:
                hm.search(mid)

        def do_linear_title_search():
            for title in titles:
                linear_exact_search(subset, title)

        def do_linear_id_search():
            for mid in ids:
                linear_exact_search_by_id(subset, mid)

        hm_title_time = _average_time(do_hm_title_search)
        hm_id_time = _average_time(do_hm_id_search)
        linear_title_time = _average_time(do_linear_title_search)
        linear_id_time = _average_time(do_linear_id_search)

        results[size] = {
            "hashmap_title": hm_title_time,
            "hashmap_id": hm_id_time,
            "linear_title": linear_title_time,
            "linear_id": linear_id_time,
        }

        print(
            f"{size:<10} {hm_title_time:<18.8f} "
            f"{hm_id_time:<16.8f} {linear_title_time:<18.8f} {linear_id_time:<16.8f}"
        )

    return results


def benchmark_prefix_search(movies: list) -> dict:
  
    print("benchmark 3 prefix search time (autocomplete)")
    print(f"  trials per measurement: {TRIALS}")
    print(f"  prefix queries: {PREFIX_QUERIES}")
    print("  theoretical: trie O(k + m), linear scan O(n)")


    header = f"{'Size':<10} {'Trie (s)':<22} {'Linear (s)':<22} {'Speedup':<12}"
    print(header)
   

    results = {}

    for size in DATASET_SIZES:
        subset = movies[:size]

        trie = Trie()
        for movie in subset:
            trie.insert(movie.title, movie)

        def do_trie_prefix():
            for prefix in PREFIX_QUERIES:
                trie.search_prefix(prefix)

        def do_linear_prefix():
            for prefix in PREFIX_QUERIES:
                linear_prefix_search(subset, prefix)

        trie_time = _average_time(do_trie_prefix)
        linear_time = _average_time(do_linear_prefix)
        speedup = linear_time / trie_time if trie_time > 0 else float('inf')

        results[size] = {
            "trie_prefix": trie_time,
            "linear_prefix": linear_time,
            "speedup": speedup,
        }

        print(f"{size:<10} {trie_time:<22.6f} {linear_time:<22.6f} {speedup:<11.2f}x")

    return results
