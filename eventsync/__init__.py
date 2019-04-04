from flask import Flask, render_template, session, url_for, flash, request, redirect
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
    LoginManager,
)
from eventsync.models import db, User
from eventsync.settings import LOGGER
import bcrypt

app = Flask(__name__)
app.config.from_object("eventsync.settings")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(str(user_id))


@app.before_first_request
def init_app():
    """Init the Database."""
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        return redirect(url_for("event_list"))
    return render_template("index.html")


@app.route("/login", methods=["POST"])
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


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["POST"])
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


@app.route("/create_account", methods=["GET"])
def create_account():
    return render_template("create_account.html")


@app.route("/event_list", methods=["GET"])
@login_required
def event_list():
    """Should return a render_template of event_list"""
    return render_template("event_list.html")


@app.route("/create_event", methods=["POST"])
@login_required
def create_event():
    """Event creation logic here

    Should return to create_event if fails, els should return to event_list
    """
    pass


if __name__ == "__main__":
    app.run()
