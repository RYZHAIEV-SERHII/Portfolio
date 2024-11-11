from flask_login import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .db import db
from .models import User, Project, Image, Skill, Experience, ContactMessage

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
    def is_accessible(self):
        # Check if the current user is authenticated and has admin privileges
        return current_user.is_authenticated and current_user.is_admin


# Add views for your models
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Project, db.session))
admin.add_view(AdminModelView(Image, db.session))
admin.add_view(AdminModelView(Skill, db.session))
admin.add_view(AdminModelView(Experience, db.session))
admin.add_view(AdminModelView(ContactMessage, db.session))
