import pytest
from spylogger import get_logger

from eventsync.app import app, db

logger = get_logger(log_level="DEBUG")


@pytest.fixture
def client():
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield client


def test_index(client):
    resp = client.get("/")
    assert b'<div class="login">' in resp.data


def test_login_with_bad_user(client):
    resp = client.post(
        "/login",
        data=dict(username="dont_exist", password="random"),
        follow_redirects=True,
    )
    assert b"User not found" in resp.data


def test_passwords_dont_match(client):
    resp = client.post(
        "/register",
        data=dict(
            password="doesntmatch", confirm_password="does", username="doesntexist"
        ),
        follow_redirects=True,
    )
    assert b"Passwords do not match" in resp.data


def test_create_user_success(client):
    resp = client.post(
        "/register",
        data=dict(password="does", confirm_password="does", username="testUser1"),
        follow_redirects=True,
    )
    assert b"Registration Complete" in resp.data
