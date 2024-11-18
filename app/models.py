from flask_login import UserMixin

from .db import db


# Define the User model
class User(UserMixin, db.Model):
    """
    User model representing a user in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password of the user.
        is_admin (bool): Indicates if the user has administrative privileges.
        created_at (datetime): Timestamp when the user was created.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    is_admin = db.Column(
        db.Boolean, default=True
    )  # Assume sole admin is true by default
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def get_id(self):
        """Return the user ID as a string."""

        return str(self.id)


# Define the Project model
class Project(db.Model):
    """
    Project model representing a project in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the project.
        user_id (int): Foreign key referencing the User model.
        title (str): Title of the project.
        description (str): Description of the project.
        tech_stack (str): Technologies used in the project.
        url (str): URL of the project.
        created_at (datetime): Timestamp when the project was created.
        project_category_id (int): Foreign key referencing the ProjectCategory model.
    """

    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    tech_stack = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    project_category_id = db.Column(
        db.Integer, db.ForeignKey("project_categories.id"), nullable=False
    )
    images = db.relationship("Image", back_populates="project")
    project_category = db.relationship("ProjectCategory", back_populates="projects")


# Define the ProjectCategory model
class ProjectCategory(db.Model):
    """
    ProjectCategory model representing a project category.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the project category.
        name (str): Name of the project category.
        projects (list[Project]): The projects associated with this category.
    """

    __tablename__ = "project_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projects = db.relationship("Project", back_populates="project_category")

    def __repr__(self):
        return f"ProjectCategory('{self.name}')"

    def __str__(self):
        return self.name


# Define the Image model
class Image(db.Model):
    """
    Image model representing an image of a project in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the image.
        project_id (int): Foreign key referencing the Project model.
        name (str): Name of the image.
        image_source (str): Source of the image (file or url).
        file_data (bytes): Binary data of the image.
        url (str): URL of the image if it is stored remotely.
        project (Project): The project this image belongs to.
    """

    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image_source = db.Column(
        db.String(50), nullable=False, default="file"
    )  # file or url
    file_data = db.Column(db.LargeBinary, nullable=True)
    url = db.Column(db.String(255), nullable=True)

    project = db.relationship("Project", back_populates="images")

    def get_image(self):
        """Return the image data or URL based on the image source."""
        return self.file_data if self.image_source == "file" else self.url

    def __str__(self):
        return self.name


# Define the Skill model
class Skill(db.Model):
    """
    Skill model representing a skill of a user in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the skill.
        user_id (int): Foreign key referencing the User model.
        skill_category_id (int): Foreign key referencing the SkillCategory model.
        skill_category (SkillCategory): The skill category this skill belongs to.
        skill_name (str): Name of the skill.
    """

    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_category_id = db.Column(
        db.Integer,
        db.ForeignKey("skill_categories.id"),
        nullable=False,
    )
    skill_category = db.relationship("SkillCategory", back_populates="skills")
    skill_name = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define the SkillCategory model
class SkillCategory(db.Model):
    """
    SkillCategory model representing a category of skills in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the skill category.
        name (str): Name of the skill category.
        skills (list[Skill]): The skills in this category.
    """

    __tablename__ = "skill_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    skills = db.relationship("Skill", back_populates="skill_category")


# Define the Experience model
class Experience(db.Model):
    """
    Experience model representing a work experience of a user in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the experience.
        user_id (int): Foreign key referencing the User model.
        company_name (str): Name of the company the user worked at.
        role (str): Role of the user in the company.
        start_date (datetime.date): Start date of the work experience.
        end_date (datetime.date): End date of the work experience.
        description (str): Description of the work experience.
    """

    __tablename__ = "experiences"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define the ContactMessage model
class ContactMessage(db.Model):
    """
    ContactMessage model representing a message from a contact form in the system.

    Attributes:
        __tablename__ (str): Name of the database table.
        id (int): Unique identifier for the contact message.
        name (str): Name of the person who sent the message.
        email (str): Email address of the person who sent the message.
        category (str): Category of the message.
        message (str): The message itself.
    """

    __tablename__ = "contact_messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"ContactMessage('{self.name}', '{self.email}', '{self.category}')"
