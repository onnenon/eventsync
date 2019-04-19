from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from eventsync.models import Event
from eventsync.settings import LOGGER

events = Blueprint("events", __name__)


@events.route("/event_list", methods=["GET"])
@login_required
def event_list():
    """Should return a render_template of event_list"""
    return render_template("event_list.html", user=current_user)


@events.route("/register_event", methods=["POST"])
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
    return redirect(url_for("event.event_list"))


@events.route("/create_event", methods=["GET"])
@login_required
def create_event():
    return render_template("create_event.html", user=current_user)


@events.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = request.form["event_id"]
    event = Event.get_event(event_id)
    if event:
        event.delete()
    flash("Event Deleted." "Success")
    return redirect(url_for("event_list"))
