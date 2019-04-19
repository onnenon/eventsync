from flask import Flask, redirect, render_template, session, url_for
from flask_login import LoginManager

from eventsync.Blueprints import register_blueprints
from eventsync.models import User, db

app = Flask(__name__)
app.config.from_object("eventsync.settings")

register_blueprints(app)

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
        return redirect(url_for("events.event_list"))
    return render_template("indextest.html")


if __name__ == "__main__":
    app.run(debug=True)
