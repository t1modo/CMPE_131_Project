from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__, template_folder="../templates")

@main_bp.route("/")
def index():
    return render_template("main/index.html")

@main_bp.route("/feature")
def feature():
    # Demo page showing base template usage
    return render_template("main/feature.html")
