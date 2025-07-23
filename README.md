# Event Planner

A simple Flask application for creating and attending events.

## Features

- User registration and JWT-based login
- Create, update and delete your own events
- RSVP to events created by others
- Search and pagination on the events list
- Export event details as `.ics` calendar files
- User profile pages showing created and attending events
- Optional script to seed the database with demo events

## Security Highlights

- Secrets such as `SECRET_KEY` and database credentials come from environment
  variables loaded via `.env`
- SQLAlchemy parameter binding guards against SQL injection
- Ownership checks before update/delete prevent IDOR issues
- Flask-Talisman sets a basic Content-Security-Policy that also allows
  Bootstrap and jQuery from their CDNs

## Software Engineering Notes

- Service layer classes encapsulate business logic
- Custom exceptions map to API-friendly error responses
- Unit tests cover routes and services

## Docker

Copy `.env.example` to `.env` and adjust credentials. Start the database container first and wait until it's ready:

```bash
docker compose up -d db
```

When the logs show "database system is ready to accept connections," run the initial migration to create the tables:

```bash
docker compose run --rm app flask db upgrade
```

Optionally seed the database with demo events to try the search feature:

```bash
docker compose run --rm app python seed_events.py
```

With the schema applied you can bring up the full stack:

```bash
docker compose up --build
```

The service listens on port 5000. Visit `http://localhost:5000` to use the app.
API endpoints live under `/api`.

## Running Tests

Execute the unit tests locally with `pytest -q`. To run them in Docker:

```bash
docker compose run --rm app pytest -q
```
