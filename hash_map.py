

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

    def _hash(self, key) -> int:
        key_str = str(key).lower()
        hash_value = 0
        prime = 31
        mod = self._capacity
        for char in key_str:
            hash_value = (hash_value * prime + ord(char)) % mod
        return hash_value

    def insert(self, key, value):
        if (self._size / self._capacity) >= self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        index = self._hash(key)
        node = self._buckets[index]

        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
