import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for

from eventsync.models import User

users = Blueprint("users", __name__)


@users.route("/create_account", methods=["GET"])
def create_account():
    return render_template("create_account.html")


@users.route("/register", methods=["POST"])
def register():
    """User registration logic here
    
    should return a redirect to either
    register, if registration fails, or to event_list if successful
    """
    username = request.form["username"]
    password = request.form["password"]

    if password != request.form["confirm_password"]:
        flash("Passwords do not match", "Error")
        return redirect(url_for("users.create_account"))

    user = User.get_user(username)
    if user is None:
        hashed = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        record = User(username=username, pw_hash=hashed)
        record.save()
        flash("Registration Complete", "Success")
    else:
        flash("User already exists.", "Error")
    return redirect(url_for("index"))
