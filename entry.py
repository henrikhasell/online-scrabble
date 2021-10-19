from online_scrabble.game import Bag, Grid, Rack, Trie, SolutionBuilder


if __name__ == "__main__":
    bag = Bag.new()
    grid = Grid.large()
    rack = Rack("avocado")
    trie = Trie.load("dictionary.txt")

    print(grid)

    solution_builder = SolutionBuilder(grid, trie)
    placements = solution_builder.solve(rack)
    for placement in placements:
        print(placement)
