import bcrypt
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from eventsync.models import User, db, Event
from eventsync.settings import LOGGER


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

from eventsync.Blueprints.login import log_in
app.register_blueprint(log_in)
from eventsync.Blueprints.logout import log_out
app.register_blueprint(log_out)
from eventsync.Blueprints.register import registeration
app.register_blueprint(registeration)
from eventsync.Blueprints.create_account import createaccount
app.register_blueprint(createaccount)

@app.route("/event_list", methods=["GET"])
@login_required
def event_list():
    """Should return a render_template of event_list"""
    return render_template("event_list.html", user=current_user)


@app.route("/register_event", methods=["POST"])
@login_required
def register_event():
    """Event creation logic here

    Should return to create_event if fails, else should return to event_list
    """
    title = request.form["title"]
    date = request.form["date"]
    time = request.form["time"]

    date_time_str = date + " " + time

    LOGGER.debug({"Date": date_time_str})
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

    event = Event(title=title, date_time=date_time, creator=current_user.username)
    event.save()
    flash("Event Created", "Success")
    return redirect(url_for("event_list"))


@app.route("/create_event", methods=["GET"])
@login_required
def create_event():
    return render_template("create_event.html", user=current_user)


@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = request.form["event_id"]
    event = Event.get_event(event_id)
    if event:
        event.delete()
    flash("Event Deleted." "Success")
    return redirect(url_for("event_list"))


if __name__ == "__main__":
    app.run(debug=True)
