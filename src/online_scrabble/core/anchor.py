from dataclasses import dataclass
from typing import List, Optional

from .grid import Grid
from .trie import Trie


@dataclass
class Anchor:
    x: int
    y: int
    x_length: int
    y_length: int
    x_trie: Trie
    y_trie: Trie


def is_anchor(grid: Grid, x: int, y: int) -> bool:
    if grid.get_tile(x, y).value is None:
        if x > 0 and grid.get_tile(x - 1, y).value is not None:
            return True
        if y > 0 and grid.get_tile(x, y - 1).value is not None:
            return True
        if x < (grid.width - 1) and grid.get_tile(x + 1, y).value is not None:
            return True
        if y < (grid.height - 1) and grid.get_tile(x, y + 1).value is not None:
            return True
    return False


def create_anchor(grid: Grid, trie: Trie, x: int, y: int) -> Optional[Anchor]:
    if not is_anchor(grid, x, y):
        return None

    i = 0
    j = 0

    x_length = 0
    y_length = 0

    x_trie = trie
    y_trie = trie

    for i in range(x - 1, -1, -1):
        if grid.get_tile(i, y).value or is_anchor(grid, i, y):
            break
        x_length += 1

    for j in range(y - 1, -1, -1):
        if grid.get_tile(x, j).value or is_anchor(grid, x, j):
            break
        y_length += 1

    if x_length == 0:
        word = grid.get_word(i, y, True)
        x_trie = trie.find(word) or trie

    if y_length == 0:
        word = grid.get_word(x, j, False)
        y_trie = trie.find(word) or trie

    return Anchor(x, y, x_length, y_length, x_trie, y_trie)


def calculate_anchors(grid: Grid, trie: Trie) -> List[Anchor]:
    anchors = []

    for y in range(grid.height):
        for x in range(grid.width):
            anchor = create_anchor(grid, trie, x, y)
            if anchor:
                anchors += [anchor]

    if not anchors:
        grid_w2 = int(grid.width / 2)
        grid_h2 = int(grid.height / 2)
        anchors += [Anchor(grid_w2, grid_h2, grid_w2, grid_h2, trie, trie)]

    return anchors
