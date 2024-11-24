from werkzeug.security import generate_password_hash

from app.db import database as db
from src.db.models import User

# Replace fields 'name', 'email', and 'password' with your credentials
name = "Portfolio_Admin"
email = "portfolio_admin@gmail.com"
password = "TypeYourPasswordHere"

# Generate a hashed password
hashed_password = generate_password_hash(password)

# Create a new user instance
new_user = User(name=name, email=email, password_hash=hashed_password, is_admin=True)

# Add the new user to the session and commit
db.session.add(new_user)
db.session.commit()
print(f"Admin {new_user.name} created successfully.")

# NOTE: This script should only be run once to initiate a new admin user for your local project

# To run this script:
# 1. Open a terminal
# 2. Open a flask shell by running `flask shell` command
# 3. Copy and paste the script's content into the flask shell
# 4. Close the flask shell
