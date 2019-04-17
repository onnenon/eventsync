import bcrypt
from flask import Flask, flash, redirect, request, url_for, Blueprint
from eventsync.models import User
from eventsync.settings import LOGGER
registeration = Blueprint('registeration',__name__)

@registeration.route("/register", methods=["POST"])
def register():
    """User registration logic here
    
    should return a redirect to either
    register, if registration fails, or to event_list if successful
    """
    username = request.form["username"]
    password = request.form["password"]

    if password != request.form["confirm_password"]:
        flash("Passwords do not match", "Error")
        return redirect(url_for("create_account"))

    user = User.get_user(username)
    if user is None:
        hashed = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        record = User(username=username, pw_hash=hashed)
        record.save()
        flash("Registration Complete", "Success")
    else:
        flash("User already exists.", "Error")
    return redirect(url_for("index"))