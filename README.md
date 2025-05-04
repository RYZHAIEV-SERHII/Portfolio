# Portfolio

![Portfolio Logo](https://i.imgur.com/OTqfqsf.png)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-Framework-brightgreen.svg)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED.svg?logo=docker)](https://www.docker.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/RYZHAIEV-SERHII/Portfolio/branch/main/graph/badge.svg)](https://codecov.io/gh/RYZHAIEV-SERHII/Portfolio)
[![Tests](https://github.com/RYZHAIEV-SERHII/Portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/RYZHAIEV-SERHII/Portfolio/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat&logo=github)](CONTRIBUTING.md)

This is my personal portfolio website built using **Python**, **Flask**, **FastAPI**, **SQLAlchemy**, and
**PostgreSQL**. The site showcases my projects, experience, and skills, while also serving as a backend API for future
integrations.

---

## Features

- **Personal Portfolio**: Showcases my skills, experience, and projects.
- **Responsive Design**: Accessible and responsive UI built with HTML, CSS, and JavaScript.
- **Database**: Utilizes PostgreSQL with SQLAlchemy for ORM and database management.
- **API Integration**: Built with FastAPI to serve endpoints for project data, projects, etc.
- **Authentication**: Secure login and admin panel to manage content.

## Tech Stack

### Backend

- **Python**: Main programming language for this project.
- **Flask**: Used for the frontend web server to handle static content, templates, and some REST API endpoints.
- **FastAPI**: Handles the API layer for handling project data and dynamic content.
- **SQLAlchemy**: ORM for database interaction with PostgreSQL.
- **PostgreSQL**: Database system used to store projects, blog posts, and other content.

### Frontend

- **HTML5 & CSS3**: Markup and styling for the website.
- **JavaScript**: Provides interactivity and improves the user experience.
- **Bootstrap**: Ensures the site is responsive and mobile-friendly.

### Deployment & DevOps

- **Docker**: Containerizes the application to ensure easy deployment and scalability.
- **Nginx**: Used as a reverse proxy server for handling web traffic efficiently.
- **Gunicorn**: A WSGI HTTP server to serve the Flask and FastAPI applications.

### Testing

- **Pytest**: Unit and integration tests for the Flask and FastAPI backends.
- **Postman**: API testing and documentation.

## Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL**
- **Docker** (optional for deployment)

## Installation

1. Clone the repository:

    ```bash
     git clone https://github.com/RYZHAIEV-SERHII/Portfolio.git
     cd Portfolio
     ```

2. Set up the environment variables:

    - Create a `.env` file in the root directory of the project.
    - Add the necessary environment variables as shown in the `.env.example` file.

3. (Option 1) Install Python dependencies manually using `uv`:

    - First, ensure you have `uv` installed. You can install it following the [official
      `uv` instructions](https://github.com/astral-sh/uv#installation).
    - Run the sync command. `uv` will automatically create a `.venv` virtual environment if one doesn't exist and
      install the dependencies defined in `pyproject.toml`:

        ```bash
        uv sync --all-extras
        ```

    - Start the applications using the project's CLI script:
        - `all`: Start both Flask (app) and FastAPI (api)

        ```bash
        python run.py start all
       ```

        - `app`: Start only Flask app

       ```bash
        python run.py start app
        ```

        - `api`: Start only FastAPI app

       ```bash
        python run.py start api
        ```

    - Stop the applications using the project's CLI script:
      - `all`: Stop both Flask (app) and FastAPI (api)

      ```bash
        python run.py stop all
      ```

      - `app`: Stop only Flask app

      ```bash
      python run.py stop app
      ```

      - `api`: Stop only FastAPI app

      ```bash
      python run.py stop api
      ```

      The Flask app will be available at `http://localhost:5000` <br>
      The FastAPI app at `http://localhost:8000`.

4. (Option 2) Start the app using Docker:

    ```bash
    docker-compose up -d
    ```

### Running Tests

```bash
pytest
```

## Project Structure

```plaintext
Portfolio/
│
├── .github/                      # GitHub configuration
│   ├── workflows/                # GitHub Actions workflows for CI/CD
│   │   ├── release.yaml          # Workflow for releases
│   │   └── tests.yml             # Workflow for running tests
│   └── codecov.yml               # Code coverage configuration
│
├── .hooks/                       # Git hooks for pre-commit checks
│   └── commit-msg                # Validates commit message format
│
├── .tools/                       # Utility scripts and tools
│   └── cp_env_to_env_example.sh  # Environment file management
│
├── alembic/                      # Database migration system
│   └── versions/                 # Migration version files
│
├── api/                          # FastAPI application code
│   ├── crud/                     # Database CRUD operations
│   │   ├── about.py              # About section operations
│   │   ├── contact.py            # Contact operations
│   │   ├── education.py          # Education operations
│   │   ├── experience.py         # Experience operations
│   │   ├── project.py            # Project operations
│   │   ├── resume.py             # Resume operations
│   │   └── skill.py              # Skills operations
│   ├── routes/                   # API endpoints
│   │   ├── about.py              # About section endpoints
│   │   ├── contact.py            # Contact endpoints
│   │   ├── education.py          # Education endpoints
│   │   ├── experiences.py        # Experience endpoints
│   │   ├── projects.py           # Project endpoints
│   │   ├── resume.py             # Resume endpoints
│   │   ├── security.py           # Authentication endpoints
│   │   └── skills.py             # Skills endpoints
│   ├── schemas/                  # Data validation models
│   ├── db.py                     # Database connection
│   ├── main.py                   # FastAPI app initialization
│   └── security.py               # Authentication utilities
│
├── app/                          # Flask application code
│   ├── static/                   # Static assets
│   │   ├── css/                  # Stylesheets
│   │   ├── img/                  # Images for portfolio
│   │   ├── js/                   # JavaScript files
│   │   └── vendor/               # Third-party libraries
│   ├── templates/                # HTML templates
│   │   ├── auth/                 # Authentication templates
│   │   ├── includes/             # Reusable components
│   │   └── projects/             # Project templates
│   ├── admin.py                  # Admin panel configuration
│   ├── auth.py                   # Authentication logic
│   ├── forms.py                  # Form definitions
│   ├── mail.py                   # Email functionality
│   └── views.py                  # Route handlers
│
├── cli/                          # Command-line interface tools
│   ├── operations.py             # CLI operations
│   └── setup.py                  # Setup utilities
│
├── docs/                         # Documentation
│   └── Enhancements.md           # Future enhancements
│
├── src/                          # Shared code between Flask and FastAPI
│   └── db/                       # Database models and services
│       ├── models.py             # SQLAlchemy models
│       └── services.py           # Database service functions
│
├── tests/                        # Test files
│
├── .dockerignore                 # Files to exclude from Docker builds
├── .env                          # Environment variables (not in version control)
├── .env.example                  # Example environment variables template
├── .gitignore                    # Files to exclude from Git
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── .python-version               # Python version specification
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── README.md                     # Project documentation
├── alembic.ini                   # Alembic configuration
├── config.py                     # Application configuration
├── docker-compose.yaml           # Docker Compose configuration
├── Dockerfile_FastAPI            # Dockerfile for FastAPI
├── Dockerfile_Flask              # Dockerfile for Flask
├── logging.conf                  # Logging configuration
├── logging_setup.py              # Logging setup utilities
├── pyproject.toml                # Project metadata and dependencies
├── run.py                        # Application entry point
└── uv.lock                       # Dependency lock file for uv package manager
```

## Future Enhancements

I have several exciting enhancements planned for the `Portfolio` project to make it even more engaging and feature-rich.

For a detailed description please refer to the [Enhancements](docs/Enhancements.md) file.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING](CONTRIBUTING.md) file
for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or suggestions,
feel free to reach out to me at [Email](mailto:rsp89@gmail.com) or [Telegram](https://t.me/CTAJIKEP)

### Happy coding!
