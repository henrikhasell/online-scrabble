from enum import Enum
from typing import List, Optional

from online_scrabble.core.bag import Bag
from online_scrabble.core.grid import Grid
from online_scrabble.core.placement import Placement, ScoredPlacement
from online_scrabble.core.player import Player
from online_scrabble.core.solution_builder import SolutionBuilder
from online_scrabble.core.rack import populate_rack, remove_letters_from_rack
from online_scrabble.core.trie import Trie


MAX_PLAYERS = 4


class GameError(Exception):
    pass


class GameState(Enum):
    WAITING_TO_START = "waiting_to_start"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PreviousPlacement:
    def __init__(self, placement: ScoredPlacement, player: str):
        self.placement = placement
        self.player = player

    def json(self):
        return {"placement": self.placement.json(), "player": self.player}

    @staticmethod
    def from_json(json_data: dict):
        return PreviousPlacement(
            ScoredPlacement.from_json(json_data["placement"]), json_data["player"]
        )


class Game:
    def __init__(
        self,
        bag: Bag,
        grid: Grid,
        players: List[Player],
        state: GameState,
        turn: Optional[str],
        previous_placement: Optional[PreviousPlacement],
    ):
        self.bag = bag
        self.grid = grid
        self.players = players
        self.state = state
        self.turn = turn
        self.previous_placement = previous_placement

    def current_player(self) -> Optional[Player]:
        if self.turn is None:
            return None

        return next((i for i in self.players if i.name == self.turn))

    def json(self) -> dict:
        return {
            "bag": self.bag.json(),
            "grid": self.grid.json(),
            "players": [i.json() for i in self.players],
            "state": self.state.value,
            "turn": self.turn,
            "previous_placement": self.previous_placement
            and self.previous_placement.json(),
        }

    def join(self, player_name: str) -> Player:
        if self.state != GameState.WAITING_TO_START:
            raise GameError("The game is in progress.")

        if len(self.players) >= MAX_PLAYERS:
            raise GameError("The game is full.")

        if player_name in (i.name for i in self.players):
            raise GameError("You already joined this game.")

        new_player = Player(player_name, populate_rack("", self.bag), 0)

        self.players += [new_player]

        return new_player

    def start(self, player_name: str) -> Player:
        if player_name not in (i.name for i in self.players):
            raise GameError("You must be in the game to start it.")

        if self.state != GameState.WAITING_TO_START:
            raise GameError("The game is in progress.")

        self.state = GameState.IN_PROGRESS
        self.turn = self.players[0].name

    def get_player(self, player_name: str) -> Player:
        player = next((i for i in self.players if i.name == player_name), None)

        if player is None:
            raise GameError("Player not in game.")

        return player

    def get_next_player(self) -> Player:
        index = None

        for index, player in enumerate(self.players):
            if player.name == self.turn:
                break

        if index is None:
            return None

        if index == len(self.players) - 1:
            return self.players[0]

        return self.players[index + 1]

    def score_placement(
        self, player_name: str, placemnt: Placement, trie: Trie
    ) -> ScoredPlacement:
        grid_copy = self.grid.copy()
        grid_copy.reset_crosscheck()

        solution_builder = SolutionBuilder(grid_copy, trie)
        player = self.get_player(player_name)

        valid_placements = solution_builder.solve(player.rack)

        expression = (i for i in valid_placements if i == placemnt)

        try:
            return next(expression)
        except StopIteration as exception:
            raise GameError("Invalid placement.") from exception

    def insert(self, player_name: str, placement: Placement, trie: Trie) -> None:
        if player_name != self.turn:
            raise GameError("It's not your turn.")

        if self.state != GameState.IN_PROGRESS:
            raise GameError("Game is not in progress.")

        scored_placement = self.score_placement(player_name, placement, trie)

        player = self.get_player(player_name)

        player.rack = remove_letters_from_rack(rack, placement.letters)
        player.rack = populate_rack(player.rack, self.bag)

        player.score += scored_placement.score

        self.grid.insert(scored_placement)
        self.turn = self.get_next_player().name

        self.previous_placement = PreviousPlacement(scored_placement, player_name)

        if len(player.rack) == 0:
            self.end_game()

    def end_game(self):
        self.state = GameState.COMPLETED
        self.turn = max(self.players, key=lambda i: i.score).name

    @staticmethod
    def new():
        bag = Bag.new()
        grid = Grid.large()
        return Game(bag, grid, [], GameState.WAITING_TO_START, None, None)
