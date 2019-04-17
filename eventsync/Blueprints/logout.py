from flask import Blueprint, redirect, url_for
from flask_login import logout_user
log_out = Blueprint('log_out',__name__)

@log_out.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))