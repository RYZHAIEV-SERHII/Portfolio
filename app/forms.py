from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
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
