import pytest
from spylogger import get_logger

from eventsync.app import app

logger = get_logger(log_level="DEBUG")


@pytest.fixture
def client():
    client = app.test_client()

    yield client


def test_index(client):
    resp = client.get("/")
    assert b'<div class="login">' in resp.data


def test_login_with_bad_user(client):
    resp = client.post("")
