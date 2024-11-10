import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
    jsonify,
)

from .db import db, convert_to_binary, write_to_file
from .forms import ContactForm
from .mail import send_email_notification
from .models import ContactMessage, Project, Image

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/about")
@main.route("/education")
@main.route("/skills")
@main.route("/projects")
def render_page():
    """
    Render the page corresponding to the route.
    """
    page = request.path.lstrip("/") or "index"  # Handles root '/' route as 'index'
    return render_template(f"{page}.html")


@main.route("/projects/<project_name>")
def project_detail(project_name):
    """
    Render the project detail page based on project name.
    """
    try:
        # Check if the template exists before rendering
        template_path = f"projects/{project_name}.html"
        return render_template(template_path)
    except Exception:
        abort(404)  # Return a 404 error if the template does not exist


@main.route("/resume")
def resume():
    """
    Redirect to resume link.
    """
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
        db.session.add(contact_message)
        db.session.commit()
        send_email_notification(name, email, category, message)
        flash("Form submitted successfully", "success")
        return redirect(url_for("main.home"))
    return render_template("contact.html", form=form)


@main.route("/add_project", methods=["POST"])
def add_project():
    """
    Add a new project along with its image to the database.
    """
    data = request.json
    new_project = Project(
        user_id=uuid.UUID(data["user_id"]),
        title=data["title"],
        description=data["description"],
        url=data["url"],
    )

    image_path = data["image_path"]
    binary_data = convert_to_binary(image_path)
    new_image = Image(name=data["image_name"], data=binary_data, project=new_project)

    db.session.add(new_project)
    db.session.add(new_image)
    db.session.commit()
    return jsonify({"message": "Project and image added successfully"}), 201


@main.route("/get_project/<uuid:project_id>", methods=["GET"])
def get_project(project_id):
    """
    Retrieve a project and its images from the database.
    """
    project = Project.query.filter_by(project_id=project_id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404

    response = {
        "title": project.title,
        "description": project.description,
        "url": project.url,
        "images": [],
    }

    for image in project.images:
        write_to_file(image.data, f"{image.name}.jpg")
        response["images"].append({"name": image.name})

    return jsonify(response), 200
