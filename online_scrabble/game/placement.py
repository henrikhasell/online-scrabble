from functools import total_ordering
from typing import List, Optional, Tuple

from .character import Character


@total_ordering
class Placement:
    def __init__(
        self,
        x: int,
        y: int,
        horizontal: bool,
        letters: List[Character]
    ):
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.letters = letters

    def __eq__(self, other) -> bool:
        return isinstance(other, Placement) and \
            self.x == other.x and \
            self.x == other.x and \
            self.y == other.y and \
            self.letters == other.letters and \
            (len(self.letters) == 1 or self.horizontal == other.horizontal)

    def __lt__(self, other) -> bool:
        if self.x == other.x:
            if self.y == other.y:
                if self.letters == other.letters:
                    return self.horizontal < other.horizontal
                return self.letters < other.letters
            return self.y < other.y
        return self.x < other.x
    
    def json(self) -> dict:
        return {
            "horizontal": self.horizontal,
            "letters": [i.json() for i in self.letters],
            "x": self.x,
            "y": self.y
        }

    @staticmethod
    def from_json(json_object: dict):
        return Placement(
            json_object['x'],
            json_object['y'],
            json_object['horizontal'],
            [Character.from_json(i) for i in json_object['letters']]
        )


def get_score(placement: Placement) -> Optional[int]:
    return getattr(placement, 'score', None)


class ScoredPlacement(Placement):
    def __init__(
        self,
        x: int,
        y: int,
        horizontal: bool,
        letters: List[Character],
        score: int
    ):
        super().__init__(
            x,
            y,
            horizontal,
            letters
        )
        self.score = score

    def __eq__(self, other) -> bool:
        score = get_score(other)
        return super().__eq__(other) if score is None else self.score == score

    def __lt__(self, other) -> bool:
        score = get_score(other)
        return super().__lt__(other) if score is None else self.score < score

    def json(self) -> dict:
        return {
            **super().json(),
            "score": self.score
        }