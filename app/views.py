from flask import Blueprint, render_template, abort

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


@main.route("/projects/<project_name>")
def project_detail(project_name):
    try:
        # Check if the template exists before rendering
        template_path = f"projects/{project_name}.html"
        return render_template(template_path)
    except Exception:
        abort(404)  # Return a 404 error if the template does not exist


@main.route("/contact")
def contact():
    return render_template("contact.html")


@main.route("/skills")
def skills():
    return render_template("skills.html")


@main.route("/education")
def education():
    return render_template("education.html")


@main.route("/resume")
def resume():
    return render_template("resume.html")
