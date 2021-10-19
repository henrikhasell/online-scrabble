import pytest

from online_scrabble.core import Bag, Character, Grid, Placement, Trie, SolutionBuilder


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
    assert True == trie.contains("avocado")


def test_trie_no_substring(trie):
    assert False == trie.contains("avoc")


def test_starting_move(solution_builder, trie):
    placements = solution_builder.solve("AVOCADO")
    assert placements[-1].score == 65


def test_grid_placement_and_fetching(grid):
    grid.insert(Placement(7, 7, True, Character.from_string("MONKEY")))
    grid.insert(Placement(9, 5, False, Character.from_string("MOKEY")))
    grid.insert(Placement(7, 8, False, Character.from_string("ONKEY")))

    print(grid)

    assert "MONKEY" == grid.get_word(7, 7, True)
    assert "MONKEY" == grid.get_word(7, 7, False)
    assert "MONKEY" == grid.get_word(12, 7, True)
    assert "MONKEY" == grid.get_word(7, 12, False)

    assert "" == grid.get_word(13, 7, True)
    assert "" == grid.get_word(7, 13, False)
