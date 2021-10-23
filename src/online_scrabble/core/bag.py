from random import randrange
from typing import List


WILD_LETTER = " "


class BagError(Exception):
    pass


class Bag:
    def __init__(self, content: List[str]):
        self.content = content

    def add_character(self, char: str, count: int) -> None:
        for _index in range(count):
            self.content += [char]

    def get_character(self) -> str:
        try:
            index = randrange(len(self.content))
        except ValueError as error:
            raise BagError("The bag is empty.") from error
        return self.content.pop(index)

    def json(self):
        return self.content

    @staticmethod
    def new():
        bag = Bag([])

        bag.add_character(WILD_LETTER, 2)

        bag.add_character("E", 12)
        bag.add_character("A", 9)
        bag.add_character("I", 9)
        bag.add_character("O", 9)
        bag.add_character("N", 6)
        bag.add_character("R", 6)
        bag.add_character("T", 6)
        bag.add_character("L", 4)
        bag.add_character("S", 4)
        bag.add_character("U", 4)

        bag.add_character("D", 4)
        bag.add_character("G", 3)

        bag.add_character("B", 2)
        bag.add_character("C", 2)
        bag.add_character("M", 2)
        bag.add_character("P", 2)

        bag.add_character("F", 2)
        bag.add_character("H", 2)
        bag.add_character("V", 2)
        bag.add_character("W", 2)
        bag.add_character("Y", 2)

        bag.add_character("K", 1)

        bag.add_character("J", 1)
        bag.add_character("X", 1)

        bag.add_character("Q", 1)
        bag.add_character("Z", 1)

        return bag
