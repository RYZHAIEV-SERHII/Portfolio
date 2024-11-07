from flask import Blueprint, render_template, request, abort, flash, redirect, url_for

from .forms import ContactForm
from .mail import send_email_notification
from .models import ContactMessage
from .models import db

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


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        category = form.category.data
        message = form.message.data
        contact_message = ContactMessage(
            name=name, email=email, category=category, message=message
        )
        db.session.add(contact_message)
        db.session.commit()
        send_email_notification(name, email, category, message)
        flash("Form submitted successfully", "success")
        return redirect(url_for("main.home"))
    return render_template("contact.html", form=form)


@main.route("/skills")
def skills():
    return render_template("skills.html")


@main.route("/education")
def education():
    return render_template("education.html")


@main.route("/resume")
def resume():
    return redirect(
        "https://drive.google.com/file/d/1fuxAUUEq0fLgF8xMh4a1IiMAl22fzEud/view?usp=drive_link"
    )
