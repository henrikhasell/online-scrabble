from functools import total_ordering


@total_ordering
class Player:
    def __init__(self, name: str, rack: str, score: int):
        self.name = name
        self.rack = rack
        self.score = score

    def json(self) -> dict:
        return {
            "name": self.name,
            "rack": list(self.rack),
            "score": self.score}

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.name < other.name
