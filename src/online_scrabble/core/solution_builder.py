from typing import List

from sortedcontainers import SortedList

from .anchor import Anchor, calculate_anchors
from .character import Character
from .grid import Grid
from .placement import Placement, ScoredPlacement
from .rack import find_in_rack
from .tile import TileType
from .trie import Trie


char_scores = {
    "A": 1,
    "B": 4,
    "C": 4,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 3,
    "H": 3,
    "I": 1,
    "J": 10,
    "K": 5,
    "L": 2,
    "M": 4,
    "N": 2,
    "O": 1,
    "P": 4,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 2,
    "V": 5,
    "W": 4,
    "X": 8,
    "Y": 3,
    "Z": 10,
}


class SolutionBuilder:
    def __init__(self, grid: Grid, trie: Trie):
        self.grid = grid
        self.trie = trie
        self.placements = SortedList()

    def cross_check(self, x: int, y: int, horizontal: bool, char: str) -> bool:
        grid_copy = self.grid.copy()
        grid_copy.get_tile(x, y).value = char
        word = grid_copy.get_word(x, y, not horizontal)
        return len(word) == 1 or self.trie.contains(word)

    def score(
        self, grid: Grid, x: int, y: int, horizontal: bool, recursive: bool = True
    ) -> int:

        if horizontal:
            while x > 0 and grid.get_tile(x - 1, y).value:
                x -= 1
        else:
            while y > 0 and grid.get_tile(x, y - 1).value:
                y -= 1

        adjacent_score = 0
        new_tile_count = 0
        tile_count = 0
        word_multiplier = 1
        word_score = 0

        while True:
            tile = grid.get_tile(x, y)

            if not tile.value:
                break

            tile_multiplier = 1

            if tile.cross_check:
                if tile.type == TileType.DOUBLE_LETTER:
                    tile_multiplier = 2
                elif tile.type == TileType.TRIPPLE_LETTER:
                    tile_multiplier = 3
                elif tile.type == TileType.DOUBLE_WORD:
                    word_multiplier = 2
                elif tile.type == TileType.TRIPPLE_WORD:
                    word_multiplier = 3

                if recursive:
                    adjacent_score += self.score(grid, x, y, not horizontal, False)

                new_tile_count += 1

            if not tile.wild:
                word_score += tile_multiplier * char_scores.get(tile.value, 0)

            tile_count += 1

            if horizontal:
                x += 1
                if x >= grid.width:
                    break
            else:
                y += 1
                if y >= grid.height:
                    break

        if new_tile_count > 0 and tile_count > 1:
            word_score *= word_multiplier
            word_score += adjacent_score

            if new_tile_count >= 7:
                word_score += 35

            return word_score

        return 0

    def legal_move(
        self,
        letters: List[Character],
        anchor: Anchor,
        horizontal: bool,
        limit: int,
    ):
        insert_x = anchor.x
        insert_y = anchor.y

        if horizontal:
            insert_x -= anchor.x_length - limit
        else:
            insert_y -= anchor.y_length - limit

        grid_copy = self.grid.copy()

        placement = Placement(insert_x, insert_y, horizontal, letters)

        grid_copy.insert(placement)

        score = self.score(grid_copy, anchor.x, anchor.y, horizontal)

        self.placements += [
            ScoredPlacement(insert_x, insert_y, horizontal, letters, score)
        ]

    def extend_right(
        self,
        rack: str,
        word: List[Character],
        segment: Trie,
        anchor: Anchor,
        horizontal: bool,
        x: int,
        y: int,
        limit: int,
    ) -> None:
        edge = x >= self.grid.width - 1 or y >= self.grid.height - 1

        if not edge:
            if horizontal:
                x += 1
            else:
                y += 1

        tile_value = self.grid.get_tile(x, y).value

        if not tile_value or edge:
            if segment.valid:
                self.legal_move(word, anchor, horizontal, limit)
            if edge:
                return
            for child in segment.children:
                character, rack_copy = find_in_rack(rack, child)
                if not character:
                    continue

                if self.cross_check(x, y, horizontal, character.value):
                    word_copy = word.copy() + [character]

                    self.extend_right(
                        rack_copy,
                        word_copy,
                        segment.children[child],
                        anchor,
                        horizontal,
                        x,
                        y,
                        limit,
                    )
        else:
            segment_continue = segment.find(tile_value)

            if segment_continue:
                self.extend_right(
                    rack, word, segment_continue, anchor, horizontal, x, y, limit
                )

    def left_part(
        self,
        rack: str,
        word: List[Character],
        segment: Trie,
        anchor: Anchor,
        horizontal: bool,
        limit: int,
    ):
        if self.cross_check(anchor.x, anchor.y, horizontal, segment.value):
            self.extend_right(
                rack, word, segment, anchor, horizontal, anchor.x, anchor.y, limit
            )

        if limit > 0:
            for child, value in segment.children.items():
                character, rack_copy = find_in_rack(rack, child)

                if not character:
                    continue

                word_copy = word.copy() + [character]

                self.left_part(
                    rack_copy,
                    word_copy,
                    value,
                    anchor,
                    horizontal,
                    limit - 1,
                )

    def solve(self, rack: str) -> SortedList[Placement]:
        self.placements = SortedList()

        anchors = calculate_anchors(self.grid, self.trie)

        for anchor in anchors:
            for key, value in anchor.x_trie.children.items():
                character, rack_copy = find_in_rack(rack, key)

                if not character:
                    continue

                self.left_part(
                    rack_copy,
                    [character],
                    value,
                    anchor,
                    True,
                    anchor.x_length,
                )

            for key, value in anchor.y_trie.children.items():
                character, rack_copy = find_in_rack(rack, key)

                if not character:
                    continue

                self.left_part(
                    rack_copy,
                    [character],
                    value,
                    anchor,
                    False,
                    anchor.y_length,
                )

        return self.placements
