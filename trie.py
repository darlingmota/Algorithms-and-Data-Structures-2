class TrieNode:
    def __init__(self):
        self.children = {}          # character -> next trienode
        self.is_end_of_word = False # True if a complete title ends here
        self.movies = []            # the actual Movie objects stored at the end


