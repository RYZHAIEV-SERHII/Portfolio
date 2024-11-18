from werkzeug.security import generate_password_hash

from app.db import db
from app.models import User

new_user = User(
    name="Portfolio_Admin", email="portfolio_admin@gmail.com", is_admin=True
)
# Replace fields 'username' and 'email' with your credentials

hashed_password = generate_password_hash(
    "TypeYourPasswordHere"
)  # Replace with your password
new_user.password_hash = hashed_password

db.session.add(new_user)
db.session.commit()
print(f"Admin {new_user.name} created successfully.")


# NOTE: This script should only be run once then initiate a new admin user for your local project

# To run this script:
# 1. Open a terminal
# 2. Open a flask shell by running `flask shell` command
# 3. Copy and paste scripts content into a flask shell
# 4. Close a flask shell
