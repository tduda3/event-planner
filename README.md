# Event Planner

A simple Flask application for creating and attending events.

## Features

- User registration and JWT-based login
- Create, update and delete your own events
- RSVP to events created by others
- Search and pagination on the events list
- Export event details as `.ics` calendar files
- User profile pages showing created and attending events

## Security Highlights

- Secrets such as `SECRET_KEY` and database credentials come from environment
  variables loaded via `.env`
- SQLAlchemy parameter binding guards against SQL injection
- Ownership checks before update/delete prevent IDOR issues
- Flask-Talisman sets a basic Content-Security-Policy

## Software Engineering Notes

- Service layer classes encapsulate business logic
- Custom exceptions map to API-friendly error responses
- Unit tests cover routes and services

## Docker Compose

A `docker-compose.yml` is included to start the app and a Postgres container.
Docker reads environment variables from a `.env` file in the project root.
Copy `.env.example` to `.env` and adjust values, then build and run everything
with:

```bash
docker compose up --build
```

Run database migrations if needed:

```bash
docker compose run --rm web flask db upgrade
```

The web service maps port 5000 and the database is exposed on port 5432.
Visit `http://localhost:5000` to use the app. API endpoints are available under
`/api`.

## Running Tests

Execute the unit tests locally with `pytest -q`. When using Docker Compose, run:

```bash
docker compose run --rm web pytest -q
```
