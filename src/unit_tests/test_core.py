# pylint: disable=redefined-outer-name
import random

import pytest

from online_scrabble.core import Bag, Character, Grid, Placement, Trie, SolutionBuilder
from online_scrabble.core.rack import populate_rack, remove_letters_from_rack


@pytest.fixture
def bag():
    return Bag.new()


@pytest.fixture
def grid():
    return Grid.large()


@pytest.fixture
def trie():
    return Trie.load("dictionary.txt")


@pytest.fixture
def solution_builder(grid, trie):
    return SolutionBuilder(grid, trie)


def test_trie_has_word(trie):
    assert trie.contains("avocado") is True


def test_trie_no_substring(trie):
    assert trie.contains("avoc") is False


def test_starting_move(solution_builder):
    placements = solution_builder.solve("AVOCADO")
    assert placements[-1].score == 65


def test_grid_placement_and_fetching(grid):
    grid.insert(Placement(7, 7, True, Character.from_string("MONKEY")))
    grid.insert(Placement(9, 5, False, Character.from_string("MOKEY")))
    grid.insert(Placement(7, 8, False, Character.from_string("ONKEY")))

    print(grid)

    assert grid.get_word(7, 7, True) == "MONKEY"
    assert grid.get_word(7, 7, False) == "MONKEY"
    assert grid.get_word(12, 7, True) == "MONKEY"
    assert grid.get_word(7, 12, False) == "MONKEY"

    assert grid.get_word(13, 7, True) == ""
    assert grid.get_word(7, 13, False) == ""


def test_solution_builder(bag, grid, solution_builder):
    random.seed(322)

    rack: str = ""

    for i in range(18):
        rack = populate_rack(rack, bag)
        placement_list = solution_builder.solve(rack)

        placement = placement_list[-1]
        grid.insert(placement)

        rack = remove_letters_from_rack(rack, placement.letters)

    print(grid)
