
#  hashmap built from scratch.

# A single node in a chain. Each bucket is a linked list of these.
class HashMapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:

    # resize once we hit 75% full 
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity: int = 1024):
        self._capacity = initial_capacity
        self._size = 0
        self._buckets = [None] * self._capacity

    # polynomial rolling hash 
    # if the key is an int i just convert it to a string first
    def _hash(self, key) -> int:
        key_str = str(key).lower()
        hash_value = 0
        prime = 31
        mod = self._capacity
        for char in key_str:
            hash_value = (hash_value * prime + ord(char)) % mod
        return hash_value

    # insert a key/value pair or update if the key already exists
    def insert(self, key, value):
        # check if we need to resize before adding
        if (self._size / self._capacity) >= self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        index = self._hash(key)
        node = self._buckets[index]

        # walk the chain if the key is already there just update the value
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        # key not in the chain so add a new node at the head
        new_node = HashMapNode(key, value)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._size += 1

    # exact lookup by key. Returns None if the key isn't found.
    def search(self, key):
        index = self._hash(key)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return None

    # remove a key. Returns True if it was deleted, False if it wasn't there.
    def delete(self, key) -> bool:
        index = self._hash(key)
        node = self._buckets[index]
        prev = None

        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[index] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return True
            prev = node
            node = node.next
        return False

    def __len__(self) -> int:
        return self._size

    # double the capacity and rehash everything
    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0  # gets recounted as we re insert

        for bucket in old_buckets:
            node = bucket
            while node is not None:
                self.insert(node.key, node.value)
                node = node.next

    # helpers

    def load_factor(self) -> float:
        return self._size / self._capacity

    # gives me chain length info so I can show the hash function isn't terrible
    def collision_stats(self) -> dict:
        chain_lengths = []
        for bucket in self._buckets:
            length = 0
            node = bucket
            while node is not None:
                length += 1
                node = node.next
            chain_lengths.append(length)

        non_empty = [l for l in chain_lengths if l > 0]
        return {
            "total_buckets": self._capacity,
            "occupied_buckets": len(non_empty),
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
            "avg_chain_length": sum(non_empty) / len(non_empty) if non_empty else 0,
            "load_factor": self.load_factor(),
        }