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


def create_account(client, username, password):
    return client.post(
        "/register",
        data=dict(password=password, confirm_password=password, username=username), follow_redirects=True)


def login(client, username, password):
    return client.post("/login",
        data=dict(username=username, password=password),
    follow_redirects=True)


def test_index(client):
    resp = client.get("/")
    assert b'<div class="login">' in resp.data


def test_login_with_bad_user(client):
    resp = login(client, "dont_exist", "random")
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
    resp = create_account(client, "TestUser1", "pass") 
    assert b"Registration Complete" in resp.data

def test_create_duplicate_user_failure(client):
    create_account(client, "testUser2", "pass")
    resp = create_account(client, "testUser2", "pass")
    assert b"User already exists." in resp.data

def test_incorrect_password(client):
    """Tests using an incorrect password

    Tests to make sure that a login fails if the wrong password
    is entered.
    """
    

    create_account(client, "testUser3", "pass")
    resp = login(client, "testUser3", "wrongpass")
    assert b"Login failed"in resp.data

def test_login_successful(client):
    """Tests user login.

    Tests that when a user is logged in successfully that they receive a flash
    message saying "You are now signed in, and that they start with no events
    created.
    """
    create_account(client, "testUser4", "pass")
    resp = login(client, "testUser4", "pass")
    assert b"You are now signed in"in resp.data
    assert b"You have no events" in resp.data

def test_create_event(client):
    """Tests event creation. 
    Tests that an event can be created, by checking to make sure a flash message is 
    recieved saying "Event created"
    
    """
    create_account(client, "testUser5", "pass")
    login(client, "testUser5", "pass")
    resp = client.post(
        "/register_event",
        data=dict(titel="Birthday", date="2019-01-01", time="13:00"),
        follow_redirects=True,
    )
    assert b"Event Created" in resp.data