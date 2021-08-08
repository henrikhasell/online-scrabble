import unittest

from online_scrabble.game import Bag, Grid, Placement, Rack, Trie, SolutionBuilder


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.bag = Bag.new()
        self.grid = Grid.large()
        self.trie = Trie.load('dictionary.txt')
        self.solution_builder = SolutionBuilder(self.grid, self.trie)

    def test_algorithm(self):
        rack = Rack('avocado')
        placements = self.solution_builder.solve(rack)

        highest_score = placements[-1].score
        self.assertEqual(highest_score, 65)