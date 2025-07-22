import pytest
from datetime import datetime
from app.services.event_service import EventService
from app.exceptions import UserValidationError, NotFoundError, PermissionError
from app.models import Event, User


def test_create_event_success(db):
    # setup: create an owner user
    owner = User(username='alice', email='alice@example.com', password_hash='hashed')
    db.session.add(owner)
    db.session.commit()

    data = {
        'title': 'Board Game Night',
        'datetime': '2025-08-01T19:30:00',
        'location': 'Community Center',
        'description': 'Bring your favorite game!'
    }
    event = EventService.create_event(owner.id, data)
    assert event.id is not None
    assert event.title == 'Board Game Night'


def test_create_event_missing_fields(db):
    with pytest.raises(UserValidationError):
        EventService.create_event(1, {'datetime': '2025-08-01T19:30:00', 'location': 'X'})
    with pytest.raises(UserValidationError):
        EventService.create_event(1, {'title': 'Test', 'location': 'X'})
    with pytest.raises(UserValidationError):
        EventService.create_event(1, {'title': 'Test', 'datetime': '2025-08-01T19:30:00'})


def test_get_event_not_found(db):
    with pytest.raises(NotFoundError):
        EventService.get_event(9999)


def test_update_event_permission(db):
    # setup two users and one event
    owner = User(username='bob', email='bob@example.com', password_hash='hashed')
    other = User(username='eve', email='eve@example.com', password_hash='hashed')
    db.session.add_all([owner, other])
    db.session.commit()
    event = EventService.create_event(owner.id, {
        'title': 'Secret Meetup',
        'datetime': '2025-09-10T18:00:00',
        'location': 'Hidden',
        'description': ''
    })
    with pytest.raises(PermissionError):
        EventService.update_event(event.id, other.id, {'title': 'Hacked'})


def test_delete_event(db):
    owner = User(username='carol', email='carol@example.com', password_hash='hashed')
    db.session.add(owner)
    db.session.commit()
    event = EventService.create_event(owner.id, {
        'title': 'Yoga Class',
        'datetime': '2025-10-05T07:00:00',
        'location': 'Park',
        'description': ''
    })
    # should not raise
    EventService.delete_event(event.id, owner.id)
    with pytest.raises(NotFoundError):
        EventService.get_event(event.id)