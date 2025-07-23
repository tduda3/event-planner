# Event Planner

A simple Flask application for creating and attending events.

## Features

- User registration and JWT-based login
- Create, update and delete your own events
- RSVP to events created by others
- Search and pagination on the events list
- Export event details as `.ics` calendar files
- User profile pages showing created and attending events

## Local Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Ensure PostgreSQL is running and accessible. Configure credentials with
   environment variables or a `.env` file:

```bash
cp .env.example .env  # then edit values as needed
```

The app looks for `DATABASE_URL`, `SECRET_KEY` and `JWT_SECRET_KEY` in the
environment. A local Postgres URL might look like:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

3. Run database migrations (optional since `db.create_all()` runs in dev):

```bash
flask db upgrade
```

4. Start the application:

```bash
flask run
```

The API is served under `/api` and the frontend is available at `http://localhost:5000`.

## Docker Compose

A `docker-compose.yml` is included to start the app and a Postgres container.
Docker reads environment variables from a `.env` file in the project root.
Copy `.env.example` to `.env` and adjust values, then build and run everything
with:

```bash
docker compose up --build
```

The web service maps port 5000 and the database is exposed on port 5432.

## Running Tests

Execute the unit tests locally with `pytest -q`. When using Docker Compose, run:

```bash
docker compose run --rm web pytest -q
```
