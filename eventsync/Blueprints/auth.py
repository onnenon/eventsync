import bcrypt
from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_user, logout_user

from eventsync.models import User
from eventsync.settings import LOGGER

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    """Authentication logic here

    If authenticated, will return a redirect to /event_list
    else will redirect to index
    """
    username = request.form["username"]
    password = request.form["password"]

    user = User.get_user(username)

    if user is None:
        flash("User not found, please create an account.", "Error")
        return redirect(url_for("index"))

    try:
        if bcrypt.checkpw(password.encode("utf8"), user.pw_hash):
            login_user(user)
            flash("You are now signed in", "Success")
            return redirect(url_for("events.event_list"))
    except Exception as e:
        LOGGER.error({"Exception", e})
    flash("Login failed", "Error")
    return redirect(url_for("index"))


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))
