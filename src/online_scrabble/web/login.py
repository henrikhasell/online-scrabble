from base64 import b64decode
from typing import Callable, Optional

from flask import make_response, Request, Response
from flask_login import LoginManager, UserMixin


class User(UserMixin):
    def __init__(self, id: str):
        self.id = id


def create_request_loader(login_manager: LoginManager) -> Callable:
    def request_loader(request: Request) -> Optional[User]:
        api_key = request.headers.get("Authorization")

        if not api_key:
            return None

        api_key = api_key.replace("Basic ", "", 1)

        try:
            api_key = b64decode(api_key).decode("utf-8")
        except UnicodeDecodeError:
            return None

        username, _password = api_key.split(":", 1)

        return User(username)

    login_manager.request_loader(request_loader)
    return request_loader


def create_unauthorized_handler(login_manager: LoginManager) -> Callable:
    def unauthorized_handler() -> Response:
        response = make_response("", 401)
        response.headers["WWW-Authenticate"] = 'Basic realm="Online Scrabble"'
        return response

    login_manager.unauthorized_handler(unauthorized_handler)
    return unauthorized_handler
