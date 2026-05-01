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
