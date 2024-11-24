from flask import flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .db import database as db
from .forms import SkillForm, ExperienceForm, ProjectForm, ImageForm
from src.db.models import (
    User,
    Project,
    Image,
    Skill,
    Experience,
    ContactMessage,
    SkillCategory,
    ProjectCategory,
)

# Initialize Flask-Admin
admin = Admin(name="Admin Panel", template_mode="bootstrap4")


def init_admin(app):
    """
    Initialize the Flask-Admin extension with the given Flask application.

    Args:
        app (Flask): The Flask application instance to initialize the admin interface with.
    """
    admin.init_app(app)


# Define custom admin views
class AdminModelView(ModelView):
    """
    Base class for all admin views. Checks if the current user is authenticated
    and has admin privileges.

    Attributes:
        column_list (tuple): List of column names to display in the list view.
        column_filters (tuple): List of column names to filter by in the list view.
    """

    def is_accessible(self):
        # Check if the current user is authenticated and has admin privileges
        return current_user.is_authenticated and current_user.is_admin


class SkillModelView(ModelView):
    """
    Admin view for the Skill model.

    Attributes:
        form (SkillForm): The form to use for creating and editing skills.
        column_labels (dict): A dictionary mapping column names to their
            corresponding labels in the list view.
        column_list (tuple): A tuple of column names to display in the list view.
        column_filters (tuple): A tuple of column names to filter by in the list view.
        column_editable_list (tuple): A tuple of column names that can be edited in the list view.
        column_formatters (dict): A dictionary of functions to format the data in the list view.
        create_skill (func): A function to create a new skill instance from the form data.
    """

    form = SkillForm
    column_labels = {"skill_category": "Category"}
    column_list = ("skill_name", "skill_category", "proficiency_level", "created_at")
    column_filters = ("skill_name", "skill_category", "proficiency_level")
    column_editable_list = ("skill_name", "skill_category", "proficiency_level")

    column_formatters = {
        "skill_category": lambda v, c, m, p: (
            m.skill_category.name if m.skill_category else ""
        )
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def create_skill(self, form: SkillForm) -> bool:
        """
        Create a new skill instance from the form data.

        Args:
            form (SkillForm): The form object containing the data.

        Returns:
            bool: True if the skill was created successfully, False otherwise.
        """
        try:
            # Create a new skill instance with the form data
            skill = Skill(
                user_id=current_user.id,
                skill_name=form.skill_name.data,
                skill_category_name=form.skill_category.data.name,
                proficiency_level=form.proficiency_level.data.name,
            )
            # Add the skill to the database session
            db.session.add(skill)
            # Commit the changes
            db.session.commit()
        except IntegrityError:
            # Rollback the session if the skill already exists
            db.session.rollback()
            flash("Error: Skill already exists.", "error")
            return False
        except Exception as e:
            # Rollback the session and flash an error message if any other exception occurs
            db.session.rollback()
            flash("Error: {}".format(e), "error")
            return False
        else:
            # Flash a success message if the skill was created successfully
            flash("Skill created successfully.", "success")
            return True


class ExperienceModelView(ModelView):
    """
    A ModelView for experiences.

    Attributes:
        form (ExperienceForm): The form to use for creating and editing experiences.
        column_labels (dict): A dictionary mapping column names to their
            corresponding labels in the list view.
        column_list (tuple): A tuple of column names to display in the list view.
        column_editable_list (tuple): A tuple of column names that can be edited in the list view.
        create_experience (func): A function to create a new experience instance from the form data.
    """

    form = ExperienceForm
    column_labels = {
        "company_name": "Company Name",
        "role": "Role",
        "start_date": "Start Date",
        "end_date": "End Date",
        "description": "Description",
    }
    column_list = (
        "company_name",
        "role",
        "start_date",
        "end_date",
        "description",
        "created_at",
    )
    column_filters = ("company_name", "role", "start_date", "end_date")
    column_editable_list = (
        "company_name",
        "role",
        "start_date",
        "end_date",
        "description",
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def create_experience(self, form: ExperienceForm) -> bool:
        """
        Creates a new experience instance from the form data.

        Args:
            form (ExperienceForm): The form containing the experience data.

        Returns:
            bool: True if the experience was created successfully, False otherwise.
        """
        try:
            # Create a new experience instance from the form data
            experience = Experience(
                user_id=current_user.id,
                company_name=form.company_name.data,
                role=form.role.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                description=form.description.data,
            )
            # Add the experience to the database session
            db.session.add(experience)
            # Commit the changes
            db.session.commit()
        except IntegrityError:
            # Rollback the session if the experience already exists
            db.session.rollback()
            flash("Error: Experience already exists.", "error")
            return False
        except Exception as e:
            # Rollback the session and flash an error message if any other exception occurs
            db.session.rollback()
            flash("Error: {}".format(e), "error")
            return False
        else:
            # Flash a success message if the experience was created successfully
            flash("Experience created successfully.", "success")
            return True


class ProjectModelView(ModelView):
    """
    Admin view for the Project model.

    Attributes:
        form (ProjectForm): The form to use for creating and editing projects.
        column_labels (dict): A dictionary mapping column names to their
            corresponding labels in the list view.
        column_list (tuple): A tuple of column names to display in the list view.
        column_filters (tuple): A tuple of column names to filter by in the list view.
        column_editable_list (tuple): A tuple of column names that can be edited in the list view.
    """

    form = ProjectForm
    column_labels = {
        "title": "Title",
        "description": "Description",
        "url": "URL",
        "tech_stack": "Tech Stack",
        "project_category": "Project Category",
        "images": "Images",
    }
    column_list = (
        "title",
        "description",
        "url",
        "tech_stack",
        "project_category",
        "created_at",
        "images",
    )
    column_filters = ("title", "description", "url", "tech_stack", "project_category")
    column_editable_list = (
        "title",
        "description",
        "url",
        "tech_stack",
        "project_category",
    )
    backref_name = "project_list"

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def create_project(self, form: ProjectForm) -> bool:
        """
        Creates a new project instance from the form data.

        Args:
            form (ProjectForm): The form containing the project data.

        Returns:
            bool: True if the project was created successfully, False otherwise.
        """
        try:
            # Create a new project instance from the form data
            project = Project(
                user_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                url=form.url.data,
                tech_stack=form.tech_stack.data,
                project_category=form.project_category.data,
            )
            # Add the project to the database session
            db.session.add(project)
            # Commit the changes
            db.session.commit()
        except IntegrityError:
            # Rollback the session if the project already exists
            db.session.rollback()
            flash("Error: Project already exists.", "error")
            return False
        except Exception as e:
            # Rollback the session and flash an error message if any other exception occurs
            db.session.rollback()
            flash("Error: {}".format(e), "error")
            return False
        else:
            # Flash a success message if the project was created successfully
            flash("Project created successfully.", "success")
            return True


class ImageView(ModelView):
    """
    Admin view for managing images associated with projects.

    Attributes:
        column_labels (dict): Maps column names to their labels in the list view.
        column_list (tuple): Columns to display in the list view.
        column_editable_list (tuple): Columns that can be edited directly in the list view.
    """

    form = ImageForm
    column_labels = {
        "id": "ID",
        "project.title": "Project",
        "image_source": "Image Source",
        "name": "File Name",
        "url": "URL",
        "file_data": "File Data",
    }
    column_list = ("id", "project.title", "image_source", "name", "url", "file_data")
    column_editable_list = ("image_source", "project", "name", "url")

    def create_image(self, form: ImageForm) -> bool:
        """
        Creates a new image instance from the form data.

        Args:
            form (ImageForm): The form containing the image data.

        Returns:
            bool: True if the image was created successfully, False otherwise.
        """
        try:
            image = Image(
                project_id=form.project.data.id,
                image_source=form.image_source.data,
                name=form.get_image_name(),
                file_data=(
                    form.file.data.read() if form.image_source.data == "file" else None
                ),
                url=form.url.data if form.image_source.data == "url" else None,
            )
            db.session.add(image)
            db.session.commit()
            flash("Image created successfully.", "success")
            return True
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating image: {e}", "error")
            return False

    def update_image(self, image: Image, form: ImageForm) -> bool:
        """
        Updates an existing image instance from the form data.

        Args:
            image (Image): The image instance to update.
            form (ImageForm): The form containing the image data.

        Returns:
            bool: True if the image was updated successfully, False otherwise.
        """
        try:
            image.project_id = form.project.data.id
            image.image_source = form.image_source.data
            image.name = form.get_image_name()
            if form.image_source.data == "file":
                image.file_data = form.file.data.read()
                image.url = None
            else:
                image.url = form.url.data
                image.file_data = None

            db.session.commit()
            flash("Image updated successfully.", "success")
            return True
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating image: {e}", "error")
            return False


# Add views for your models
admin.add_view(AdminModelView(User, db.session))
admin.add_view(ProjectModelView(Project, db.session))
admin.add_view(AdminModelView(ProjectCategory, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(SkillModelView(Skill, db.session))
admin.add_view(AdminModelView(SkillCategory, db.session))
admin.add_view(ExperienceModelView(Experience, db.session))
admin.add_view(AdminModelView(ContactMessage, db.session))
