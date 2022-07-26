import argparse
from base64 import b64encode
from enum import Enum
from time import sleep
from typing import List, Optional

import requests

from online_scrabble.core import Grid, Placement, ScoredPlacement, SolutionBuilder, Trie


HOST = "http://localhost:8000"

GAME_NAME = "game1"


class GameState(Enum):
    InProgress = "in_progress"
    WaitingToStart = "waiting_to_start"
    Completed = "completed"


class BotError(Exception):
    pass


class ScrabbleBot:
    def __init__(self, name: str):
        self.name = name

        self.grid = None
        self.rack = None
        self.score = None
        self.state = None
        self.turn = None
        self.number_of_players = None

        self.trie = Trie.load("dictionary.txt")

    def get_headers(self):
        authorization = b64encode(f"{self.name}:".encode("utf-8")).decode("utf-8")

        return {"Authorization": authorization}

    def put_placement(self, game: str, placement: Placement):
        response = requests.put(
            f"{HOST}/game/{game}/placement",
            headers=self.get_headers(),
            json=placement.json(),
        )

        response_json = response.json()

        if "message" in response_json:
            raise BotError(response_json["message"])

        self.rack = response_json["rack"]
        self.score = response_json["score"]
        print(placement.json())

    def fetch_game(self, game: str):
        response = requests.get(f"{HOST}/game/{game}", headers=self.get_headers())
        response_json = response.json()

        if "message" in response_json:
            raise BotError(response_json["message"])

        self.state = GameState(response_json["state"])
        self.grid = Grid.from_json(response_json["grid"])
        self.turn = response_json["turn"]
        self.number_of_players = len(response_json["players"])

    def our_turn(self) -> bool:
        return self.state is GameState.InProgress and self.turn == self.name

    def create_game(self, game: str):
        response = requests.post(f"{HOST}/game/{game}", headers=self.get_headers())
        response_json = response.json()

        message = response_json["message"]

        if message == "Game created.":
            self.fetch_game(game)
        else:
            raise BotError(message)

    def join_game(self, game: str):
        response = requests.put(f"{HOST}/game/{game}/join", headers=self.get_headers())

        response_json = response.json()

        if "message" in response_json:
            raise BotError(response_json["message"])

        self.rack = response_json["rack"]
        self.score = response_json["score"]

    def get_player_state(self, game: str):
        response = requests.put(
            f"{HOST}/game/{game}/player_state", headers=self.get_headers()
        )

        response_json = response.json()

        if "message" in response_json:
            raise BotError(response_json["message"])

        self.rack = response_json["rack"]
        self.score = response_json["score"]

    def start_game(self, game: str):
        response = requests.put(f"{HOST}/game/{game}/start", headers=self.get_headers())

        response_json = response.json()

        if "message" in response_json:
            raise BotError(response_json["message"])

    def get_highest_scoring_move(self, rack: List[str]) -> Optional[ScoredPlacement]:
        solution_builder = SolutionBuilder(self.grid, self.trie)
        placements = solution_builder.solve("".join(rack))

        if len(placements) == 0:
            return None

        return placements[-1]

    def work(self, game: str):
        if (
            self.turn is None
            and type(self.number_of_players) is int
            and self.number_of_players >= 2
        ):
            try:
                self.start_game(game)
            except BotError:
                pass

        self.fetch_game(game)

        if self.our_turn():
            if self.rack is None:
                self.get_player_state(game)

            placement = self.get_highest_scoring_move(self.rack)

            if placement is not None:
                self.put_placement(game, placement)
            else:
                print("No valid placement found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    scrabble_bot = ScrabbleBot(args.name)
    print(f"Creating + joining {GAME_NAME}...")

    try:
        scrabble_bot.create_game(GAME_NAME)
    except BotError as e:
        print(e)

    try:
        scrabble_bot.join_game(GAME_NAME)
    except BotError as e:
        print(e)

    while True:
        try:
            scrabble_bot.work(GAME_NAME)
        except BotError as e:
            print(e)
