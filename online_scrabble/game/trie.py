from typing import Optional


class Trie:
    def __init__(self, word: Optional[str] = None):
        self.children = {}

        if word:
            self.value = word[0]
            self.valid = len(word) == 1
        else:
            self.value = None
            self.valid = False

        if word and not self.valid:
            self.insert(word[1:])

    def find(self, word: str):
        if len(word) == 0:
            return None

        char = word[0].upper()

        if char not in self.children:
            return None
        elif len(word) > 1:
            return self.children[char].find(word[1:])
        else:
            return self.children[char]

    def contains(self, word: str) -> bool:
        trie = self.find(word)
        return trie is not None and trie.valid

    def insert(self, word: str) -> None:
        char = word[0].upper()

        if char not in self.children:
            self.children.update({char: Trie(word)})
        elif len(word) > 1:
            self.children[char].insert(word[1:])

    @staticmethod
    def load(path: str):
        trie = Trie()

        with open(path) as f:
            for word in [i[:-1] for i in f]:
                trie.insert(word)

        return trie
