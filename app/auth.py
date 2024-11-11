from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from .forms import LoginForm
from .models import User

login_manager = LoginManager()  # Create a LoginManager instance

auth_bp = Blueprint("auth", __name__)


def init_login_manager(app):
    """
    Initialize the Flask-Login extension with the given Flask application.

    Args:
        app (Flask): The Flask application instance to initialize the login manager with.
    """
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle the login process, including rendering the login form and processing the submission.

    GET: Render the login form.
    POST: Process the form submission and attempt to log in the user.

    Returns:
        str: The rendered HTML template in case of a GET request.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("main.render_page"))
        else:
            flash("Login failed. Check your email and password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Log out the current user and redirect back to the main page.

    This endpoint requires an active login session.

    Returns:
        str: The rendered HTML template for the main page.
    """
    logout_user()
    return redirect(url_for("main.render_page"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
