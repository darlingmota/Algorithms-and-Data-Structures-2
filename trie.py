class TrieNode:
    def __init__(self):
        self.children = {}          # character -> next trienode
        self.is_end_of_word = False # True if a complete title ends here
        self.movies = []            # the actual Movie objects stored at the end


class Trie:

    def __init__(self):
        self._root = TrieNode()
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


    def search_prefix(self, prefix: str, max_results: int = 50) -> list:
        prefix_key = prefix.lower()
        node = self._root

        for char in prefix_key:
            if char not in node.children:
                return []  # prefix doesn't exist
            node = node.children[char]

        results = []
        self._collect_all(node, results, max_results)
        return results

    def _collect_all(self, node: TrieNode, results: list, max_results: int):
        if len(results) >= max_results:
            return

        if node.is_end_of_word:
            results.extend(node.movies)

        for child in node.children.values():
            if len(results) >= max_results:
                break
            self._collect_all(child, results, max_results)

    def search_exact(self, title: str) -> list:
        key = title.lower()
        node = self._root

        for char in key:
            if char not in node.children:
                return []
            node = node.children[char]

        return node.movies if node.is_end_of_word else []
