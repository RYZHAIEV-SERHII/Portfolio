from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/projects")
def projects():
    return render_template("projects.html")


@main.route("/contact")
def contact():
    return render_template("contact.html")
