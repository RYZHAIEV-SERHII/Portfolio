from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask app.

    :param app: Flask application instance
    """
    db.init_app(app)


def convert_to_binary(file_path):
    """
    Convert an image file to binary data.

    :param file_path: Path to the image file
    :return: Binary data of the image
    """
    with open(file_path, "rb") as file:
        binary_data = file.read()
    return binary_data


def write_to_file(binary_data, output_path):
    """
    Write binary data to an image file.

    :param binary_data: Binary data to write
    :param output_path: Path to save the image file
    """
    with open(output_path, "wb") as file:
        file.write(binary_data)
