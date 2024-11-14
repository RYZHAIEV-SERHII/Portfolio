from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    RadioField,
    EmailField,
    HiddenField,
    SelectField,
)
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import SkillCategory


class ContactForm(FlaskForm):
    """
    Form for sending a contact message.
    """

    category = RadioField(
        "I'm interested in ...",
        choices=[
            ("web_development", "Web Development"),
            ("hiring", "Hiring"),
            ("freelance", "Freelance"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField("Email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10)])


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (EmailField): Field for user's email address.
        password (PasswordField): Field for user's password.
        submit (SubmitField): Submit button for the form.
    """

    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SkillForm(FlaskForm):
    """
    Form for adding a new skill.

    Attributes:
        skill_name (StringField): Field for the name of the skill.
        skill_category (QuerySelectField): Field for the category of the skill.
        proficiency_level (SelectField): Field for the proficiency level of the skill.
        user_id (HiddenField): Field for the user ID the skill belongs to.
    """

    skill_name = StringField("Skill Name", validators=[DataRequired()])
    skill_category = QuerySelectField(
        "Skill Category",
        query_factory=lambda: SkillCategory.query.all(),
        get_label=lambda x: x.name,
        validators=[DataRequired()],
    )
    proficiency_level = SelectField(
        "Proficiency Level",
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
            ("Expert", "Expert"),
        ],
        validators=[DataRequired()],
    )
    user_id = HiddenField(
        "User ID", default=lambda: current_user.id if current_user else None
    )
