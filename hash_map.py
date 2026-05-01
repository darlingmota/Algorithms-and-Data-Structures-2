class HashMapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity: int = 1024):
        self._capacity = initial_capacity
        self._size = 0
        self._buckets = [None] * self._capacity
