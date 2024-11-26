from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from src.db import Base


class User(Base, UserMixin):
    """Represents a user entity in the database.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): Username chosen by the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password of the user.
        is_admin (bool): Whether the user is an admin or not.
        created_at (datetime): Timestamp when the user was created.
        skills (list[Skill]): List of associated skills.
        experiences (list[Experience]): List of associated experiences.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=True)  # Assume sole admin is true by default
    created_at = Column(DateTime, default=func.current_timestamp())
    skills = relationship("Skill", backref="user")
    experiences = relationship("Experience", backref="user")

    def __init__(self, name, email, password_hash, is_admin=True):
        """Constructor for the User model.

        Args:
            name (str): Name of the user.
            email (str): Email address of the user.
            password_hash (str): Hashed password of the user.
            is_admin (bool): Indicates if the user has administrative privileges.
        """
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    def get_id(self):
        """Return the user ID as a string.

        Returns:
            str: The user ID.
        """
        return str(self.id)


class Project(Base):
    """Project model representing a project in the system.

    Attributes:
        id (int): Unique identifier for the project.
        user_id (int): Foreign key referencing the User model.
        title (str): Title of the project.
        description (str): Description of the project.
        tech_stack (str): Technologies used in the project.
        url (str): URL of the project.
        created_at (datetime): Timestamp when the project was created.
        project_category_id (int): Foreign key referencing the ProjectCategory model.
        images (list[Image]): List of associated images.
        project_category (ProjectCategory): The category this project belongs to.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    tech_stack = Column(String(255))
    url = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    project_category_id = Column(
        Integer, ForeignKey("project_categories.id"), nullable=False
    )

    images = relationship("Image", back_populates="project")
    project_category = relationship("ProjectCategory", back_populates="projects")

    def __init__(
        self, user_id, title, description, tech_stack, url, project_category_id
    ):
        """Constructor for the Project model.

        Args:
            user_id (int): Foreign key referencing the User model.
            title (str): Title of the project.
            description (str): Description of the project.
            tech_stack (str): Technologies used in the project.
            url (str): URL of the project.
            project_category_id (int): Foreign key referencing the ProjectCategory model.
        """
        self.user_id = user_id
        self.title = title
        self.description = description
        self.tech_stack = tech_stack
        self.url = url
        self.project_category_id = project_category_id


class ProjectCategory(Base):
    """ProjectCategory model representing a category of projects in the system.

    Attributes:
        id (int): Unique identifier for the project category.
        name (str): Name of the project category.
        projects (list[Project]): The projects associated with this category.
    """

    __tablename__ = "project_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    projects = relationship("Project", back_populates="project_category")

    def __init__(self, name):
        """Initialize a ProjectCategory instance.

        Args:
            name (str): Name of the project category.
        """
        self.name = name

    def __repr__(self):
        """Return a string representation of the ProjectCategory instance.

        Returns:
            str: A string representing the ProjectCategory instance.
        """
        return f"ProjectCategory('{self.name}')"

    def __str__(self):
        """Return the name of the project category.

        Returns:
            str: The name of the project category.
        """
        return self.name


class Image(Base):
    """Image model representing an image in the system.

    Attributes:
        id (int): Unique identifier for the image.
        name (str): Name of the image.
        url (str): URL of the image.
        image_category_id (int): Foreign key referencing the image category
            this image belongs to.
        project_id (int, optional): Foreign key referencing the project this image
            belongs to, if any.
        project (Project): The project this image belongs to, if any.
        image_category (ImageCategory): The image category this image belongs to.
    """

    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    image_category_id = Column(
        Integer, ForeignKey("image_categories.id"), nullable=False
    )
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="images")
    image_category = relationship("ImageCategory", back_populates="images")

    def __init__(self, name, url, image_category_id, project_id=None):
        """Initialize an Image instance.

        Args:
            name (str): Name of the image.
            url (str): URL of the image.
            image_category_id (int): Foreign key referencing the image category
                this image belongs to.
            project_id (int, optional): Foreign key referencing the project this image
                belongs to, if any.
        """
        self.name = name
        self.url = url
        self.image_category_id = image_category_id
        self.project_id = project_id

    def get_image(self) -> str:
        """Return the URL of the image.

        Returns:
            str: The URL of the image.
        """
        return self.url

    def __str__(self) -> str:
        """Return the name of the image.

        Returns:
            str: The name of the image.
        """
        return self.name


class ImageCategory(Base):
    """ImageCategory model representing a category of images in the system.

    Attributes:
        id (int): Unique identifier for the image category.
        name (str): Name of the image category.
        images (list[Image]): The images in this category.
    """

    __tablename__ = "image_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    images = relationship("Image", back_populates="image_category")

    def __init__(self, name):
        """Initialize an ImageCategory instance.

        Args:
            name (str): Name of the image category.
        """
        self.name = name

    def __str__(self):
        """Return the name of the image category.

        Returns:
            str: The name of the image category.
        """
        return self.name


class Skill(Base):
    """Skill model representing a skill of a user in the system.

    Attributes:
        id (int): Unique identifier for the skill.
        user_id (int): Foreign key referencing the User model.
        skill_category_id (int): Foreign key referencing the SkillCategory model.
        skill_name (str): Name of the skill.
        proficiency_level (str): Proficiency level of the user in the skill.
        created_at (datetime): Timestamp when the skill was created.
        skill_category (SkillCategory): The skill category this skill belongs to.
    """

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_category_id = Column(
        Integer, ForeignKey("skill_categories.id"), nullable=False
    )
    skill_name = Column(String(50), nullable=False)
    proficiency_level = Column(String(50))
    created_at = Column(DateTime, default=func.current_timestamp())

    skill_category = relationship("SkillCategory", back_populates="skills")

    def __init__(self, user_id, skill_category_id, skill_name, proficiency_level=None):
        """Initialize a Skill instance.

        Args:
            user_id (int): Foreign key referencing the User model.
            skill_category_id (int): Foreign key referencing the SkillCategory model.
            skill_name (str): Name of the skill.
            proficiency_level (str, optional): Proficiency level of the user in the skill.
        """
        self.user_id = user_id
        self.skill_category_id = skill_category_id
        self.skill_name = skill_name
        self.proficiency_level = proficiency_level


class SkillCategory(Base):
    """SkillCategory model representing a category of skills in the system.

    Attributes:
        id (int): Unique identifier for the skill category.
        name (str): Name of the skill category.
        skills (list[Skill]): The skills in this category.
    """

    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    skills = relationship("Skill", back_populates="skill_category")

    def __init__(self, name):
        """Initialize a SkillCategory instance.

        Args:
            name (str): Name of the skill category.
        """
        self.name = name


class Experience(Base):
    """Experience model representing a work experience of a user in the system.

    Attributes:
        id (int): Unique identifier for the experience.
        user_id (int): Foreign key referencing the User model.
        company_name (str): Name of the company the user worked at.
        role (str): Role of the user in the company.
        start_date (datetime): Start date of the work experience.
        end_date (datetime): End date of the work experience.
        description (str): Description of the work experience.
        created_at (datetime): Timestamp when the experience was created.
    """

    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())

    def __init__(self, user_id, company_name, role, start_date, end_date, description):
        """Initialize an Experience instance.

        Args:
            user_id (int): Foreign key referencing the User model.
            company_name (str): Name of the company the user worked at.
            role (str): Role of the user in the company.
            start_date (datetime): Start date of the work experience.
            end_date (datetime): End date of the work experience.
            description (str): Description of the work experience.
        """
        self.user_id = user_id
        self.company_name = company_name
        self.role = role
        self.start_date = start_date
        self.end_date = end_date
        self.description = description


class ContactMessage(Base):
    """ContactMessage model representing a message from a contact form in the system.

    Attributes:
        id (int): Unique identifier for the contact message.
        name (str): Name of the person who sent the message.
        email (str): Email address of the person who sent the message.
        category (str): Category of the message.
        message (str): The message itself.
    """

    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)

    def __init__(self, name, email, category, message):
        """Initialize a ContactMessage instance.

        Args:
            name (str): Name of the person who sent the message.
            email (str): Email address of the person who sent the message.
            category (str): Category of the message.
            message (str): The message itself.
        """
        self.name = name
        self.email = email
        self.category = category
        self.message = message

    def __repr__(self) -> str:
        """Return a string representation of the ContactMessage instance.

        Returns:
            str: A string representing the ContactMessage instance.
        """
        return f"ContactMessage('{self.name}', '{self.email}', '{self.category}')"
