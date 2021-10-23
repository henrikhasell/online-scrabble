from enum import Enum
from typing import Optional

from colorama import Back


class TileType(Enum):
    NOMRAL = "normal"
    DOUBLE_LETTER = "double_letter"
    DOUBLE_WORD = "double_word"
    TRIPPLE_LETTER = "triple_letter"
    TRIPPLE_WORD = "triple_word"
    START = "start"


colour_map = {
    TileType.NOMRAL: Back.LIGHTBLACK_EX,
    TileType.DOUBLE_LETTER: Back.LIGHTBLUE_EX,
    TileType.DOUBLE_WORD: Back.LIGHTRED_EX,
    TileType.TRIPPLE_LETTER: Back.LIGHTGREEN_EX,
    TileType.TRIPPLE_WORD: Back.LIGHTYELLOW_EX,
    TileType.START: Back.LIGHTMAGENTA_EX,
}


class Tile:
    def __init__(
            self,
            type_: TileType,
            value: Optional[str],
            wild: bool,
            cross_check: bool):
        self.type = type_
        self.value = value
        self.wild = wild
        self.cross_check = cross_check

    def json(self) -> dict:
        return {
            "type": self.type.value,
            "value": self.value,
            "wild": self.wild,
            "cross_check": self.cross_check,
        }

    def __str__(self) -> str:
        tile_colour = colour_map[self.type]
        return f'{tile_colour}{self.value or " "}'

    @staticmethod
    def from_json(json_data):
        return Tile(
            TileType(json_data["type"]),
            json_data["value"],
            json_data["wild"],
            json_data["cross_check"],
        )
