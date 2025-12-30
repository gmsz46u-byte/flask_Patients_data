from flask import Blueprint, render_template
from flask_login import login_required

deleting_page = Blueprint("deleting_page",__name__)

@deleting_page.route("/deleting_page")
@login_required
def index():
    return render_template("deleting_page.html")