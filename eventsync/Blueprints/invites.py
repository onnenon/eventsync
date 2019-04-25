from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from eventsync.models import User, BelongTo

invites = Blueprint("invites", __name__)

@invites.route("/member_list", methods=["GET"])
@login_required
def member_list():
    # get people from database
    users = User.get_all_but_user(current_user.username)
    event_id = request.args.get("event_id")
    return render_template("member_list.html", users=users, event_id=event_id)

@invites.route("/send_invite", methods=["POST"])
@login_required
def send_invite():
    username = request.form["username"]
    event_id = request.form["event_id"]

    belongTo = BelongTo(username=username, eventID=event_id)
    belongTo.save()

    flash("User added to event", "Success")
    return redirect(url_for("events.event_list"))



