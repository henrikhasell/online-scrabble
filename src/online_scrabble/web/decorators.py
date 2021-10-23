from functools import wraps
from typing import Callable

from flask_login import login_required
from flask_restx import Api


def api_login_required(api: Api) -> Callable:
    def decorator(func: Callable) -> Callable:
        @api.param("Authorization",
                   '"Basic" authentication (RFC-7617).',
                   "header")
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs) -> Callable:
            return func(*args, **kwargs)

        return wrapper

    return decorator
