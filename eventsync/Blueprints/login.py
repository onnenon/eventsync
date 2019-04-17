import bcrypt
from flask import Flask, flash, redirect, request, url_for, Blueprint
from flask_login import login_user
from eventsync.models import User
from eventsync.settings import LOGGER

log_in = Blueprint('log_in',__name__)

@log_in.route("/login", methods=["POST"])
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
            return redirect(url_for("event_list"))
    except Exception as e:
        LOGGER.error({"Exception", e})
    flash("Login failed", "Error")
    return redirect(url_for("index"))