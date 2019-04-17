from flask import render_template, Blueprint
createaccount = Blueprint('createaccount',__name__)

@createaccount.route("/create_account", methods=["GET"])
def create_account():
    return render_template("create_account.html")