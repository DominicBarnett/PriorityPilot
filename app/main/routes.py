from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("main/index.html")

@main_bp.route("/landing")
def landing():
    return render_template("main/landing-page.html")

@main_bp.route("/contact")
def contact():
    return render_template("main/contact-us.html")