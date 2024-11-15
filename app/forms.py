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
    DateField,
)
from wtforms.validators import DataRequired, Length, URL
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import SkillCategory, ProjectCategory


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


class ExperienceForm(FlaskForm):
    """
    Form for adding a new experience.

    Attributes:
        company_name (StringField): Field for the name of the company.
        role (StringField): Field for the role in the company.
        start_date (DateField): Field for the start date of the experience.
        end_date (DateField): Field for the end date of the experience.
        description (TextAreaField): Field for the description of the experience.
        user_id (HiddenField): Field for the user ID the experience belongs to.
    """

    company_name = StringField("Company Name", validators=[DataRequired()])
    role = StringField("Role", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date")
    description = TextAreaField("Description", validators=[DataRequired()])

    user_id = HiddenField(
        "User ID", default=lambda: current_user.id if current_user else None
    )


class ProjectForm(FlaskForm):
    """
    Form for adding a new project.

    Attributes:
        title (StringField): Field for the title of the project.
        description (TextAreaField): Field for the description of the project.
        url (StringField): Field for the URL of the project.
        tech_stack (StringField): Field for the tech stack used in the project.
        project_category (QuerySelectField): Field for the project category.
        user_id (HiddenField): Field for the user ID the project belongs to.
    """

    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    tech_stack = StringField("Tech Stack", validators=[DataRequired()])
    project_category = QuerySelectField(
        "Project Category",
        query_factory=lambda: ProjectCategory.query.all(),
        get_label=lambda x: x.name,
    )
    user_id = HiddenField(
        "User ID", default=lambda: current_user.id if current_user else None
    )
