# tests/services/test_registration_service.py
import pytest
from datetime import datetime
from app.services.registration_service import RegistrationService
from app.exceptions import UserValidationError, NotFoundError, PermissionError
from app.models import Event, User, Registration


def test_register_for_event_success(db):
    # Setup a user and event
    user = User(username='u1', email='u1@example.com', password_hash='x')
    event = Event(
        title='E1',
        datetime=datetime.fromisoformat('2025-08-01T10:00:00'),
        location='L1',
        description='',
        owner_id=1
    )
    db.session.add_all([user, event])
    db.session.commit()

    reg = RegistrationService.register_for_event(user.id, event.id)
    assert isinstance(reg, Registration)
    assert reg.user_id == user.id
    assert reg.event_id == event.id


def test_register_missing_event(db):
    with pytest.raises(NotFoundError):
        RegistrationService.register_for_event(1, 999)


def test_register_duplicate(db):
    user = User(username='u2', email='u2@example.com', password_hash='x')
    event = Event(
        title='E2',
        datetime=datetime.fromisoformat('2025-08-02T10:00:00'),
        location='L2',
        description='',
        owner_id=1
    )
    db.session.add_all([user, event])
    db.session.commit()
    RegistrationService.register_for_event(user.id, event.id)
    with pytest.raises(UserValidationError):
        RegistrationService.register_for_event(user.id, event.id)


def test_cancel_registration_success(db):
    user = User(username='u3', email='u3@example.com', password_hash='x')
    event = Event(
        title='E3',
        datetime=datetime.fromisoformat('2025-08-03T10:00:00'),
        location='L3',
        description='',
        owner_id=1
    )
    db.session.add_all([user, event])
    db.session.commit()
    reg = RegistrationService.register_for_event(user.id, event.id)
    # cancel
    RegistrationService.cancel_registration(reg.id, user.id)
    with pytest.raises(NotFoundError):
        RegistrationService.cancel_registration(reg.id, user.id)


def test_cancel_other_user(db):
    u1 = User(username='u4', email='u4@example.com', password_hash='x')
    u2 = User(username='u5', email='u5@example.com', password_hash='x')
    event = Event(
        title='E4',
        datetime=datetime.fromisoformat('2025-08-04T10:00:00'),
        location='L4',
        description='',
        owner_id=1
    )
    db.session.add_all([u1, u2, event])
    db.session.commit()
    reg = RegistrationService.register_for_event(u1.id, event.id)
    with pytest.raises(PermissionError):
        RegistrationService.cancel_registration(reg.id, u2.id)