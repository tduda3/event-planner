# tests/conftest.py
import os
import sys
import pytest

# Ensure the app package is importable when tests are run without installation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db as _db

@pytest.fixture(scope='session')
def app():
    """Create Flask app for tests."""
    return create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

@pytest.fixture(scope='session')
def db(app):
    """Initialize and tear down the database once per session."""
    with app.app_context():
        _db.create_all()
    yield _db
    with app.app_context():
        _db.drop_all()

@pytest.fixture(autouse=True)
def reset_db(app, db):
    """Push app context, reset schema, and keep context open for each test."""
    ctx = app.app_context()
    ctx.push()
    _db.drop_all()
    _db.create_all()
    yield
    _db.session.remove()
    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """Provide a Flask test client."""
    return app.test_client()
