from flask import flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from src.db.models import (
    User,
    Project,
    Image,
    Skill,
    Experience,
    ContactMessage,
    SkillCategory,
    ProjectCategory,
    ImageCategory,
    Resume,
    Certification,
)
from .db import database as db
from .forms import (
    SkillForm,
    ExperienceForm,
    ProjectForm,
    ImageForm,
    ImageCategoryForm,
    ResumeForm,
    CertificationForm,
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
        "name": "Name",
        "url": "URL",
        "image_category": "Image Category",
        "project": "Project",
    }
    column_list = ("name", "url", "image_category", "project")
    column_editable_list = ("name", "url", "image_category", "project")

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
                name=form.get_image_name(),
                url=form.url.data,
                image_category_id=form.image_category.data,
                project_id=form.project.data,
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
            image.name = form.get_image_name()
            image.url = form.url.data

            db.session.commit()
            flash("Image updated successfully.", "success")
            return True
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating image: {e}", "error")
            return False


class ImageCategoryView(AdminModelView):
    """
    Admin view for managing image categories.

    Attributes:
        column_labels (dict): Maps column names to their labels in the list view.
        column_list (tuple): Columns to display in the list view.
        column_editable_list (tuple): Columns that can be edited directly in the list view.
    """

    form = ImageCategoryForm
    column_labels = {"name": "Name"}
    column_list = ("name",)
    column_editable_list = ("name",)


class ResumeModelView(AdminModelView):
    """
    Admin view for the Resume model.

    Attributes:
        form (ResumeForm): The form to use for creating and editing resumes.
        column_list (tuple): Columns to display in the list view.
        column_labels (dict): Maps column names to their labels in the list view.
        column_formatters (dict): Functions to format data in the list view.
    """

    form = ResumeForm
    column_list = ("id", "user", "link", "created_at")
    column_labels = {
        "id": "ID",
        "user": "User",
        "link": "Link",
        "created_at": "Created At",
    }
    column_formatters = {
        "user": lambda v, c, m, p: m.user.name if m.user else "",
    }

    def get_query(self):
        """
        Override the default query to include a join with the User model.

        Returns:
            Query: A SQLAlchemy query object.
        """
        return self.session.query(self.model).join(User)

    def get_count_query(self):
        """
        Override the default count query to include a join with the User model.

        Returns:
            Query: A SQLAlchemy query object for counting rows.
        """
        return self.session.query(db.func.count("*")).select_from(self.model).join(User)

    def create_resume(self, form: ResumeForm) -> bool:
        """
        Creates a new resume instance from the form data.

        Args:
            form (ResumeForm): The form containing the resume data.

        Returns:
            bool: True if the resume was created successfully, False otherwise.
        """
        try:
            # Create a new resume instance
            resume = Resume(user_id=current_user.id, link=form.link.data)
            # Add the resume to the database session
            db.session.add(resume)
            # Commit the changes
            db.session.commit()
            flash("Resume created successfully.", "success")
            return True
        except Exception as e:
            # Rollback the session and flash an error message if an exception occurs
            db.session.rollback()
            flash(f"Error creating resume: {e}", "error")
            return False

    def update_resume(self, resume: Resume, form: ResumeForm) -> bool:
        """
        Updates an existing resume instance from the form data.

        Args:
            resume (Resume): The resume instance to update.
            form (ResumeForm): The form containing the resume data.

        Returns:
            bool: True if the resume was updated successfully, False otherwise.
        """
        try:
            # Update the resume link
            resume.link = form.link.data
            # Commit the changes
            db.session.commit()
            flash("Resume updated successfully.", "success")
            return True
        except Exception as e:
            # Rollback the session and flash an error message if an exception occurs
            db.session.rollback()
            flash(f"Error updating resume: {e}", "error")
            return False


class CertificationModelView(ModelView):
    """
    Admin view for the Certification model.

    Attributes:
        form (CertificationForm): The form to use for creating and editing certifications.
        column_list (tuple): A tuple of column names to display in the list view.
        column_filters (tuple): A tuple of column names to filter by in the list view.
        column_editable_list (tuple): A tuple of column names that can be edited in the list view.
    """

    form = CertificationForm
    column_list = (
        "name",
        "issuing_organization",
        "issue_date",
        "credential_id",
        "credential_url",
        "skills_acquired",
    )
    column_filters = ("name", "issuing_organization", "issue_date")
    column_editable_list = (
        "name",
        "issuing_organization",
        "issue_date",
        "credential_id",
        "credential_url",
        "skills_acquired",
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def create_model(self, form):
        try:
            certification = Certification(
                user_id=current_user.id,
                name=form.name.data,
                issuing_organization=form.issuing_organization.data,
                issue_date=form.issue_date.data,
                credential_id=form.credential_id.data,
                credential_url=form.credential_url.data,
                skills_acquired=form.skills_acquired.data,
            )
            db.session.add(certification)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Error: Certification already exists.", "error")
            return False
        except Exception as e:
            db.session.rollback()
            flash("Error: {}".format(e), "error")
            return False
        else:
            flash("Certification created successfully.", "success")
            return True


# Add views for your models
admin.add_view(AdminModelView(User, db.session))
admin.add_view(ProjectModelView(Project, db.session))
admin.add_view(AdminModelView(ProjectCategory, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(ImageCategoryView(ImageCategory, db.session))
admin.add_view(SkillModelView(Skill, db.session))
admin.add_view(AdminModelView(SkillCategory, db.session))
admin.add_view(ExperienceModelView(Experience, db.session))
admin.add_view(AdminModelView(ContactMessage, db.session))
admin.add_view(ResumeModelView(Resume, db.session))
admin.add_view(CertificationModelView(Certification, db.session))
