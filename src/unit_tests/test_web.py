# pylint: disable=redefined-outer-name
import pytest

from online_scrabble.web import __main__ as main


@pytest.fixture
def app():
    return main.app.test_client()


@pytest.fixture
def grid():
    return Grid.large()


def test_app(app):
    response = app.get("/")
    assert b"<title>Online Scrabble</title>" in response.data
    assert 200 == response.status_code
