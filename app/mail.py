import os

from dotenv import load_dotenv
from flask_mail import Mail, Message

load_dotenv()

# Initialize the Flask-Mail extension
mail = Mail()


def init_mail(app):
    """
    Initialize the Flask-Mail extension with the given Flask application.

    Parameters:
        app (Flask): The Flask application instance to initialize the mail extension with.
    """
    mail.init_app(app)


def send_email_notification(name, email, category, message):
    msg = Message(
        f"New {category.capitalize()} Message",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[os.getenv("MAIL_USERNAME")],
    )
    msg.body = f"Name: {name}\nEmail: {email}\nCategory: {category}\nMessage: {message}"
    mail.send(msg)
