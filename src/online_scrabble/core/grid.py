from typing import List

from colorama import Fore, Style

from online_scrabble.core.placement import Placement
from online_scrabble.core.tile import Tile, TileType


class Grid:
    def __init__(self, width: int, height: int, tiles: List[Tile]):
        self.width = width
        self.height = height
        self.tiles = tiles

    def json(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "tiles": [i.json() for i in self.tiles],
        }

    def __str__(self) -> str:
        result = ""
        for y in range(self.height):
            result += Fore.WHITE

            for x in range(self.width):
                tile = self.get_tile(x, y)
                result += str(tile)

            result += f"{Style.RESET_ALL}"

            if y < self.height - 1:
                result += "\n"

        return result

    def get_word(self, x: int, y: int, horizontal: bool) -> str:
        if self.get_tile(x, y).value is None:
            return ""

        result = ""

        if horizontal:
            while x > 0 and self.get_tile(x - 1, y).value:
                x -= 1
            while x < self.width:
                tile = self.get_tile(x, y)
                if not tile.value:
                    break
                result += tile.value
                x += 1
        else:
            while y > 0 and self.get_tile(x, y - 1).value:
                y -= 1
            while y < self.height:
                tile = self.get_tile(x, y)
                if not tile.value:
                    break
                result += tile.value
                y += 1

        return result

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[y * self.width + x]

    def insert(self, placement: Placement) -> None:
        self.reset_crosscheck()
        index = 0

        letters = placement.letters
        x = placement.x
        y = placement.y

        while index < len(letters) and x < self.width and y < self.height:
            tile = self.get_tile(x, y)

            if not tile.value:
                character = letters[index]
                index += 1

                tile.cross_check = True
                tile.value = character.value
                tile.wild = character.wild

            if placement.horizontal:
                x += 1
            else:
                y += 1

    def copy(self):
        tiles = list(map(lambda i: Tile(i.type, i.value,
                                        i.wild, i.cross_check), self.tiles))
        return Grid(self.width, self.height, tiles)

    def reset_crosscheck(self):
        for x in range(self.width):
            for y in range(self.height):
                self.get_tile(x, y).cross_check = False

    @staticmethod
    def empty(width: int, height: int):
        tiles = list(
            map(
                lambda i: Tile(TileType.NOMRAL, None, False, False),
                range(width * height),
            )
        )
        return Grid(width, height, tiles)

    @staticmethod
    def large():
        grid = Grid.empty(15, 15)

        grid.get_tile(3, 0).type = TileType.TRIPPLE_WORD
        grid.get_tile(6, 0).type = TileType.TRIPPLE_LETTER
        grid.get_tile(8, 0).type = TileType.TRIPPLE_LETTER
        grid.get_tile(11, 0).type = TileType.TRIPPLE_WORD

        grid.get_tile(2, 1).type = TileType.DOUBLE_LETTER
        grid.get_tile(5, 1).type = TileType.DOUBLE_WORD
        grid.get_tile(9, 1).type = TileType.DOUBLE_WORD
        grid.get_tile(12, 1).type = TileType.DOUBLE_LETTER

        grid.get_tile(1, 2).type = TileType.DOUBLE_LETTER
        grid.get_tile(4, 2).type = TileType.DOUBLE_LETTER
        grid.get_tile(10, 2).type = TileType.DOUBLE_LETTER
        grid.get_tile(13, 2).type = TileType.DOUBLE_LETTER

        grid.get_tile(0, 3).type = TileType.TRIPPLE_WORD
        grid.get_tile(3, 3).type = TileType.TRIPPLE_LETTER
        grid.get_tile(7, 3).type = TileType.DOUBLE_WORD
        grid.get_tile(11, 3).type = TileType.TRIPPLE_LETTER
        grid.get_tile(14, 3).type = TileType.TRIPPLE_WORD

        grid.get_tile(2, 4).type = TileType.DOUBLE_LETTER
        grid.get_tile(6, 4).type = TileType.DOUBLE_LETTER
        grid.get_tile(8, 4).type = TileType.DOUBLE_LETTER
        grid.get_tile(12, 4).type = TileType.DOUBLE_LETTER

        grid.get_tile(1, 5).type = TileType.DOUBLE_WORD
        grid.get_tile(5, 5).type = TileType.TRIPPLE_LETTER
        grid.get_tile(9, 5).type = TileType.TRIPPLE_LETTER
        grid.get_tile(13, 5).type = TileType.DOUBLE_WORD

        grid.get_tile(0, 6).type = TileType.TRIPPLE_LETTER
        grid.get_tile(4, 6).type = TileType.DOUBLE_LETTER
        grid.get_tile(10, 6).type = TileType.DOUBLE_LETTER
        grid.get_tile(14, 6).type = TileType.TRIPPLE_LETTER

        grid.get_tile(3, 7).type = TileType.DOUBLE_WORD
        grid.get_tile(7, 7).type = TileType.START
        grid.get_tile(11, 7).type = TileType.DOUBLE_WORD

        grid.get_tile(0, 8).type = TileType.TRIPPLE_LETTER
        grid.get_tile(4, 8).type = TileType.DOUBLE_LETTER
        grid.get_tile(10, 8).type = TileType.DOUBLE_LETTER
        grid.get_tile(14, 8).type = TileType.TRIPPLE_LETTER

        grid.get_tile(1, 9).type = TileType.DOUBLE_WORD
        grid.get_tile(5, 9).type = TileType.TRIPPLE_LETTER
        grid.get_tile(9, 9).type = TileType.TRIPPLE_LETTER
        grid.get_tile(13, 9).type = TileType.DOUBLE_WORD

        grid.get_tile(2, 10).type = TileType.DOUBLE_LETTER
        grid.get_tile(6, 10).type = TileType.DOUBLE_LETTER
        grid.get_tile(8, 10).type = TileType.DOUBLE_LETTER
        grid.get_tile(12, 10).type = TileType.DOUBLE_LETTER

        grid.get_tile(0, 11).type = TileType.TRIPPLE_WORD
        grid.get_tile(3, 11).type = TileType.TRIPPLE_LETTER
        grid.get_tile(7, 11).type = TileType.DOUBLE_WORD
        grid.get_tile(11, 11).type = TileType.TRIPPLE_LETTER
        grid.get_tile(14, 11).type = TileType.TRIPPLE_WORD

        grid.get_tile(1, 12).type = TileType.DOUBLE_LETTER
        grid.get_tile(4, 12).type = TileType.DOUBLE_LETTER
        grid.get_tile(10, 12).type = TileType.DOUBLE_LETTER
        grid.get_tile(13, 12).type = TileType.DOUBLE_LETTER

        grid.get_tile(2, 13).type = TileType.DOUBLE_LETTER
        grid.get_tile(5, 13).type = TileType.DOUBLE_WORD
        grid.get_tile(9, 13).type = TileType.DOUBLE_WORD
        grid.get_tile(12, 13).type = TileType.DOUBLE_LETTER

        grid.get_tile(3, 14).type = TileType.TRIPPLE_WORD
        grid.get_tile(6, 14).type = TileType.TRIPPLE_LETTER
        grid.get_tile(8, 14).type = TileType.TRIPPLE_LETTER
        grid.get_tile(11, 14).type = TileType.TRIPPLE_WORD

        return grid

    @staticmethod
    def from_json(json_data: dict):
        return Grid(
            json_data["width"],
            json_data["height"],
            [Tile.from_json(i) for i in json_data["tiles"]],
        )
