# `Portfolio`

This is my personal portfolio website built using **Python**, **Flask**, **FastAPI**, **SQLAlchemy**, and
**PostgreSQL**. The site showcases my projects, experience, and skills, while also serving as a backend API for future
integrations.

---

## Features

- **Personal Portfolio**: Showcases my skills, experience, and projects.
- **Blog**: A space to share articles, tutorials, and thoughts.
- **API Integration**: Built with FastAPI to serve endpoints for project data, blog posts, etc.
- **Database**: Utilizes PostgreSQL with SQLAlchemy for ORM and database management.
- **Authentication**: Secure login and admin panel to manage content.
- **Responsive Design**: Accessible and responsive UI built with HTML, CSS, and JavaScript.

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

- **Python 3.8+**
- **PostgreSQL**
- **Docker** (optional for deployment)
- **Node.js** (optional for frontend dependencies)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RYZHAIEV-SERHII/Portfolio.git
    cd Portfolio
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start the Flask server:
    ```bash
    flask run
    ```

4. Start the FastAPI server:
    ```bash
    uvicorn api:app --reload
    ```

5. (Optional) Start the app in Docker:
    ```bash
    docker-compose up
    ```

### Running Tests

```bash
pytest
```

## Folder Structure

```bash
portfolio-site/
│
├── app/                # Flask app with templates and static files
├── api/                # FastAPI app for API endpoints
├── models/             # SQLAlchemy models and database configuration
├── tests/              # Test cases for the backend
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── README.md
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
