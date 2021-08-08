from enum import Enum
from typing import Optional

from colorama import Back


class TileType(Enum):
    Normal = 'normal'
    DoubleLetter = 'double_letter'
    DoubleWord = 'double_word'
    TripleLetter = 'triple_letter'
    TripleWord = 'triple_word'
    Start = 'start'


colour_map = {
    TileType.Normal: Back.LIGHTBLACK_EX,
    TileType.DoubleLetter: Back.LIGHTBLUE_EX,
    TileType.DoubleWord: Back.LIGHTRED_EX,
    TileType.TripleLetter: Back.LIGHTGREEN_EX,
    TileType.TripleWord: Back.LIGHTYELLOW_EX,
    TileType.Start: Back.LIGHTMAGENTA_EX,
}


class Tile:
    def __init__(
            self,
            type: TileType,
            value: Optional[str],
            wild: bool,
            cross_check: bool):
        self.type = type
        self.value = value
        self.wild = wild
        self.cross_check = cross_check

    def json(self) -> dict:
        return {
            'type': self.type.value,
            'value': self.value,
            'wild': self.wild,
            'cross_check': self.cross_check
        }

    def __str__(self) -> str:
        tile_colour = colour_map[self.type]
        return f'{tile_colour}{self.value or " "}'

    @staticmethod
    def from_json(json_data):
        return Tile(
            TileType(json_data['type']),
            json_data['value'],
            json_data['wild'],
            json_data['cross_check']
        )
