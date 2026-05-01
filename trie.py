
# custom prefix trie built from scratch.


# A single node in the trie. one node per character.
class TrieNode:
    def __init__(self):
        self.children = {}          # character -> next trienode
        self.is_end_of_word = False # True if a complete title ends here
        self.movies = []            # the actual Movie objects stored at the end


class Trie:

    def __init__(self):
        self._root = TrieNode()
        self._size = 0  # how many titles we've inserted


    # O(k) time where k is the length of the title
    def insert(self, title: str, movie):
        key = title.lower()
        node = self._root

        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True
        node.movies.append(movie)
        self._size += 1

    # main autocomplete operation returns every movie whose title starts with prefix

    def search_prefix(self, prefix: str, max_results: int = 50) -> list:
        prefix_key = prefix.lower()
        node = self._root

        # walk down to the end of the prefix
        for char in prefix_key:
            if char not in node.children:
                return []  # prefix doesn't exist
            node = node.children[char]

        # now collect everything in the subtree below this node
        results = []
        self._collect_all(node, results, max_results)
        return results

    # recursive helper goes through the subtree and pulls out all the movies
    def _collect_all(self, node: TrieNode, results: list, max_results: int):
        if len(results) >= max_results:
            return

        if node.is_end_of_word:
            results.extend(node.movies)

        for child in node.children.values():
            if len(results) >= max_results:
                break
            self._collect_all(child, results, max_results)

    # exact title match  O(k)
    def search_exact(self, title: str) -> list:
        key = title.lower()
        node = self._root

        for char in key:
            if char not in node.children:
                return []
            node = node.children[char]

        return node.movies if node.is_end_of_word else []

    # quick check does any title start with this prefix?
    def starts_with(self, prefix: str) -> bool:
        key = prefix.lower()
        node = self._root

        for char in key:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def __len__(self) -> int:
        return self._size