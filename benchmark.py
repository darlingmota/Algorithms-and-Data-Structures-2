
import time
import random
import tracemalloc

from hash_map import HashMap
from trie import Trie


TRIALS = 5


DATASET_SIZES = [500, 1000, 2000, 5000, 10000, 20000, 27278]

PREFIX_QUERIES = ["the", "star", "da", "a", "love", "man", "night", "dark", "war", "inc"]

EXACT_QUERY_COUNT = 20



def _average_time(func, trials: int = TRIALS) -> float:
    times = []
    for _ in range(trials):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)
