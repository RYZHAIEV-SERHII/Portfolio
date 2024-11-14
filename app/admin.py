from flask import flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .db import db
from .forms import SkillForm, ExperienceForm
from .models import (
    User,
    Project,
    Image,
    Skill,
    Experience,
    ContactMessage,
    SkillCategory,
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


# Add views for your models
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Project, db.session))
admin.add_view(AdminModelView(Image, db.session))
admin.add_view(SkillModelView(Skill, db.session))
admin.add_view(ExperienceModelView(Experience, db.session))
admin.add_view(AdminModelView(ContactMessage, db.session))
admin.add_view(AdminModelView(SkillCategory, db.session))
