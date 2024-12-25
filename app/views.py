from urllib.parse import unquote

from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
)

from logging_setup import app_logger
from src.db.models import ContactMessage, Project
from .db import database
from .forms import ContactForm
from .mail import send_email_notification

main = Blueprint("main", __name__)


@main.route("/<page>")
@main.route("/")
def render_page(page="index"):
    """
    Render the page based on the current route.
    If route is one of the predefined routes: ("index", "about", "education", "skills", "projects")
    then render the corresponding template.
    """
    try:
        if page == "projects":
            projects = database.session.query(Project).all()
            return render_template("projects.html", projects=projects)
        else:
            return render_template(
                f"{page}.html"
            )  # If no page is specified, default to "index"
    except Exception as e:
        app_logger.error("Template does not exist")
        app_logger.error(f"Details: {str(e)}")
        abort(404)  # Return 404 if the template does not exist


@main.route("/projects/<project_name>")
def project_detail(project_name):
    """
    Render the project detail page based on project name.
    """
    try:
        # Decode the project name from the URL
        decoded_project_name = unquote(project_name)

        # Query the project by its title
        project = (
            database.session.query(Project)
            .filter_by(title=decoded_project_name)
            .first()
        )

        if not project:
            app_logger.error("Project not found")
            app_logger.error(f"Details: {project_name}")
            abort(404)  # Return a 404 error if the project is not found

        return render_template("projects/project_detail.html", project=project)
    except Exception as e:
        app_logger.error("Error rendering project detail page")
        app_logger.error(f"Details: {str(e)}")
        abort(404)  # Return a 404 error if the template does not exist


@main.route("/resume")
def resume():
    """
    Redirect to resume link.
    """
    app_logger.info("Redirecting to resume link")
    return redirect(
        "https://drive.google.com/file/d/1fuxAUUEq0fLgF8xMh4a1IiMAl22fzEud/view?usp=drive_link"
    )


@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Handle contact form submission.
    """
    form = ContactForm()
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        category = form.category.data
        message = form.message.data
        contact_message = ContactMessage(
            name=name, email=email, category=category, message=message
        )
        database.session.add(contact_message)
        database.session.commit()
        send_email_notification(name, email, category, message)
        flash("Form submitted successfully", "success")
        app_logger.info("Contact form submitted successfully")
        return redirect(url_for("main.render_page"))
    return render_template("contact.html", form=form)
