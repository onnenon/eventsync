from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from eventsync.models import User

invites = Blueprint("invites", __name__)

@invites.route("/member_list", methods=["GET"])
@login_required
def member_list():
    # get people from database
    users = User.get_all_but_user(current_user.username)
    return render_template("member_list.html", users=users)

@invites.route("/send_invite", methods=["POST"])
@login_required
def send_invite():
    

