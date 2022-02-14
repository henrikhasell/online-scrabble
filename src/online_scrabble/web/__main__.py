import random

from flask import abort, Flask
from flask_login import current_user, LoginManager
from flask_restx import Api, fields, marshal, Resource

from online_scrabble.core import (
    Placement,
    Player,
    ScoredPlacement,
    Trie,
)
from online_scrabble.web.decorators import api_login_required
from online_scrabble.web.game import Game, GameError
from online_scrabble.web.login import create_request_loader, create_unauthorized_handler


app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"] = False

api = Api(
    app,
    version="0.1",
    title="Online Scrabble",
    description="To play with friends.",
    validate=True,
)

game_namespace = api.namespace("Game", path="/game")
action_namespace = api.namespace("Action", path="/game/<id>")

login_manager = LoginManager()
login_manager.init_app(app)
create_request_loader(login_manager)
create_unauthorized_handler(login_manager)

dictionary = Trie.load("dictionary.txt")
game_map = {}


game_id_description = "Game ID."


model_tile = api.model(
    "Tile",
    {
        "type": fields.String(
            enum=[
                "normal",
                "double_letter",
                "double_word",
                "tripple_letter",
                "tripple_word",
                "start",
            ],
            required=True,
        ),
        "cross_check": fields.Boolean(required=True),
        "value": fields.String(required=True),
        "wild": fields.Boolean(required=True),
    },
)

model_player = api.model(
    "Player",
    {
        "name": fields.String(example="John", required=True),
        "score": fields.Integer(example=0, required=True),
    },
)

model_grid = api.model(
    "Grid",
    {
        "tiles": fields.List(fields.Nested(model_tile, required=True), required=True),
        "width": fields.Integer(required=True),
        "height": fields.Integer(required=True),
    },
)

model_character = api.model(
    "Character",
    {
        "value": fields.String(example="A", required=True),
        "wild": fields.Boolean(example=False, required=True),
    },
)


model_placement = api.model(
    "Placement",
    {
        "horizontal": fields.Boolean(example=True, required=True),
        "letters": fields.List(
            fields.Nested(model_character, required=True), required=True
        ),
        "x": fields.Integer(example=7, required=True),
        "y": fields.Integer(example=7, required=True),
    },
)


model_scored_placement = api.inherit(
    "ScoredPlacement", model_placement, {"score": fields.Integer(required=True)}
)


model_previous_placement = api.model(
    "PreviousPlacement",
    {
        "placement": fields.Nested(model_scored_placement, required=True),
        "player": fields.String(required=True),
    },
)


model_game = api.model(
    "Game",
    {
        "grid": fields.Nested(model_grid, required=True),
        "players": fields.List(
            fields.Nested(model_player, required=True), required=True
        ),
        "previous_placement": fields.Nested(model_previous_placement, allow_null=True),
        "state": fields.String(
            enum=["waiting_to_start", "in_progress", "completed"], required=True
        ),
        "turn": fields.String(),
    },
)

model_message = api.model("Message", {"message": fields.String(required=True)})

model_player_state = api.model(
    "PlayerState",
    {
        "rack": fields.List(fields.String(example="A", required=True), required=True),
        "score": fields.Integer(required=True),
    },
)

model_game_and_player_state = api.model(
    "GameAndPlayerState",
    {
        "game": fields.Nested(model_game, required=True),
        "player_state": fields.Nested(model_player_state),
    },
)


def create_game(id: str) -> None:
    if game_map.get(id):
        abort(400, "Game already exists.")
    game_map[id] = Game.new()


def get_game(id: str) -> Game:
    game = game_map.get(id)
    if not game:
        abort(404, "This game does not exist.")
    return game


def place_game(id: str, placement: Placement) -> Player:
    game = get_game(id)

    try:
        game.insert(current_user.get_id(), placement, dictionary)
    except GameError as error:
        abort(400, str(error))

    return get_player(id)


def score_placement(id: str, placement: Placement) -> ScoredPlacement:
    game = get_game(id)

    try:
        return game.score_placement(current_user.get_id(), placement, dictionary)
    except GameError as error:
        abort(400, str(error))


def join_game(id: str) -> Player:
    game = get_game(id)

    try:
        player = game.join(current_user.get_id())
    except GameError as error:
        abort(400, str(error))

    return player


def start_game(id: str) -> Game:
    game = get_game(id)

    try:
        game.start(current_user.get_id())
    except GameError as error:
        abort(400, str(error))

    return game


def get_player(id: str) -> Player:
    game = get_game(id)

    try:
        player = game.get_player(current_user.get_id())
    except GameError as error:
        abort(400, str(error))

    return player


def delete_game(id: str) -> None:
    get_game(id)
    game_map[id] = None


@game_namespace.route("/<id>")
@game_namespace.param("id", game_id_description)
class GameResource(Resource):
    @api_login_required(api)
    @api.doc(
        responses={
            200: ["Game created.", "Message"],
            400: ["Game already exists.", "Message"],
            401: ["Unauthorized.", "Message"],
        }
    )
    @api.marshal_with(model_message)
    def post(self, id: str):
        """Create a new game."""
        create_game(id)
        return {"message": "Game created."}

    @game_namespace.marshal_with(model_game, code=200)
    @game_namespace.response(404, "Game does not exist.")
    def get(self, id: str):
        """Get game information."""
        return get_game(id).json()

    @api_login_required(api)
    @game_namespace.response(200, "Game was deleted.")
    @game_namespace.response(404, "Game does not exist.")
    @game_namespace.response(401, "Unauthorized.")
    def delete(self, id: str):
        """Delete an existing game."""
        delete_game(id)
        return {"message": "Success."}


@action_namespace.route("/join")
@game_namespace.param("id", game_id_description)
class ActionJoinResource(Resource):
    @api_login_required(api)
    @action_namespace.doc(
        responses={
            200: ["Successfully joined game.", "PlayerState"],
            400: ["Failed to join game.", "Message"],
            401: ["Unauthorized.", "Message"],
            404: ["Game does not exist.", "Message"],
        }
    )
    def put(self, id: str):
        player = join_game(id)
        player_json = player.json()
        return marshal(player_json, model_player_state)


@action_namespace.route("/placement")
@action_namespace.param("id", game_id_description)
class ActionPlacementResource(Resource):
    @api_login_required(api)
    @action_namespace.expect(model_placement)
    @action_namespace.doc(
        responses={
            200: ["Placement successful.", "PlayerState"],
            400: ["Invalid placement.", "Message"],
            401: ["Unauthorized.", "Message"],
            404: ["Game does not exist.", "Message"],
        }
    )
    def put(self, id: str):
        placement = Placement.from_json(api.payload)

        return marshal(place_game(id, placement).json(), model_player_state)


@action_namespace.route("/player_state")
@action_namespace.param("id", game_id_description)
class ActionPlayerStateResource(Resource):
    @api_login_required(api)
    @action_namespace.doc(
        responses={
            200: ["Player state", "PlayerState"],
            400: ["Player not in game.", "Message"],
            401: ["Unauthorized.", "Message"],
            404: ["Game does not exist.", "Message"],
        }
    )
    def put(self, id: str):
        player = get_player(id)
        player_json = player.json()
        return marshal(player_json, model_player_state)


@action_namespace.route("/start")
@game_namespace.param("id", game_id_description)
class ActionStartGameResource(Resource):
    @api_login_required(api)
    @api.doc(
        responses={
            200: ["Success.", "Game"],
            400: ["Game in progres.", "Message"],
            401: ["Unauthorized.", "Message"],
            404: ["Game does not exist.", "Message"],
        }
    )
    def put(self, id: str):
        game = start_game(id)
        return marshal(game.json(), model_game)


@action_namespace.route("/score_placement")
@action_namespace.param("id", game_id_description)
class ActionScorePlacement(Resource):
    @action_namespace.expect(model_placement)
    @api_login_required(api)
    @api.doc(
        responses={
            200: ["Success.", "ScoredPlacement"],
            400: ["Invalid placement.", "Message"],
            404: ["Game does not exist.", "Message"],
        }
    )
    def put(self, id_: str):
        placement = Placement.from_json(api.payload)
        return marshal(score_placement(id_, placement).json(), model_scored_placement)


if __name__ == "__main__":
    random.seed(0)
    app.run()
