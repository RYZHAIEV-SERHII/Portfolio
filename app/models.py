import uuid

from sqlalchemy.dialects.postgresql import UUID

from .db import db


# Define the User model
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define the Project model
class Project(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    images = db.relationship("Image", back_populates="project")


# Define the Image model
class Image(db.Model):
    __tablename__ = "images"
    image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("projects.project_id"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    project = db.relationship("Project", back_populates="images")


# Define the Skill model
class Skill(db.Model):
    __tablename__ = "skills"
    skill_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False
    )
    skill_name = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define the Experience model
class Experience(db.Model):
    __tablename__ = "experiences"
    experience_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False
    )
    company_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Define the ContactMessage model
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"ContactMessage('{self.name}', '{self.email}', '{self.category}')"
