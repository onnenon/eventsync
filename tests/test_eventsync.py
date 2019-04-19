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

def test_create_duplicate_user_failure(client):
    client.post(
        "/register",
        data=dict(password="does", confirm_password="does", username="testUser2"),
        follow_redirects=True,
    )
    resp = client.post(
        "/register",
        data=dict(password="does", confirm_password="does", username="testUser2"),
        follow_redirects=True,
    )
    assert b"User already exists." in resp.data

def test_incorrect_password(client):
    client.post(
        "/register",
        data=dict(password="does", confirm_password="does", username="testUser3"),
        follow_redirects=True,
    )
    resp = client.post(
        "/login",
        data=dict(password="incorrect", username="testUser3"),
        follow_redirects=True,
    )
    assert b"Login failed"in resp.data

def test_login_successful(client):
    """Tests user login.

    Tests that when a user is logged in successfully that they receive a flash
    message saying "You are now signed in, and that they start with no events
    created.
    """
    client.post(
        "/register",
        data=dict(password="does", confirm_password="does", username="testUser4"),
        follow_redirects=True,
    )
    resp = client.post(
        "/login",
        data=dict(password="does", username="testUser4"),
        follow_redirects=True,
    )
    assert b"You are now signed in"in resp.data
    assert b"You have no events" in resp.data