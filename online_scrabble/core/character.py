from functools import total_ordering


@total_ordering
class Character:
    def __init__(self, value: str, wild: bool):
        self.value = value
        self.wild = wild

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.wild == other.wild

    def __lt__(self, other) -> bool:
        if self.value == other.value:
            return self.wild < other.wild
        return self.value < other.value

    def json(self) -> dict:
        return {"value": self.value, "wild": self.wild}

    @staticmethod
    def from_json(json_object: dict):
        return Character(json_object["value"], json_object["wild"])

    @staticmethod
    def from_string(input_: str):
        return [Character(i, False) for i in input_]
