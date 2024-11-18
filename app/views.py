from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
    jsonify,
    session,
)

from .db import db, write_to_file
from .forms import ContactForm
from .mail import send_email_notification
from .models import ContactMessage, Project, Image, Experience

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
        return render_template(
            f"{page}.html"
        )  # If no page is specified, default to "index"
    except Exception:
        abort(404)  # Return 404 if the template does not exist


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
        return redirect(url_for("main.render_page"))
    return render_template("contact.html", form=form)


@main.route("/add_project", methods=["POST"])
def add_project():
    """
    Add a new project along with its image to the database.
    """
    data = request.get_json()
    try:
        new_project = Project(
            user_id=data.get("user_id"),
            title=data.get("title"),
            description=data.get("description"),
            url=data.get("url"),
        )

        image_data = request.get_data()
        new_image = Image(
            name=data.get("image_name"), data=image_data, project=new_project
        )

        db.session.add(new_project)
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"message": "Project and image added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@main.route("/get_project/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """
    Retrieve a project and its images from the database.
    """
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404

    response = {
        "title": project.title,
        "description": project.description,
        "url": project.url,
        "images": [{"name": image.name} for image in project.images],
    }

    for image in project.images:
        write_to_file(image.data, f"{image.name}.jpg")

    return jsonify(response), 200


@main.route("/admin/experiences", methods=["POST"])
def create_experience():
    user_id = session.get("user_id")
    if user_id is None:
        # Handle the case where the user is not logged in
        return "Error: User is not logged in"
    experience = Experience(user_id=user_id, **request.form.to_dict())
    db.session.add(experience)
    db.session.commit()
    return "Experience created successfully"


@main.route("/images")
def images():
    projects = Project.query.all()
    return render_template("images.html", projects=projects)
