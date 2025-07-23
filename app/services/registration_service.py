# app/services/registration_service.py
from app.models import Registration, Event
from app import db
from app.exceptions import UserValidationError, NotFoundError, PermissionError

class RegistrationService:
    """Service layer for event RSVP (registrations)."""

    @staticmethod
    def register_for_event(user_id: int, event_id: int) -> Registration:
        """Sign up a user for an event."""
        # Ensure event exists
        event = Event.query.get(event_id)
        if not event:
            raise NotFoundError(f'Event with id {event_id} not found')
        # Prevent duplicate registration
        existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing:
            raise UserValidationError('Already registered for this event')
        # Create registration
        reg = Registration(user_id=user_id, event_id=event_id)
        db.session.add(reg)
        db.session.commit()
        return reg

    @staticmethod
    def cancel_registration(registration_id: int, user_id: int) -> None:
        """Cancel a registration if owned by user."""
        reg = Registration.query.get(registration_id)
        if not reg:
            raise NotFoundError(f'Registration with id {registration_id} not found')
        if reg.user_id != user_id:
            raise PermissionError('Cannot cancel registration for another user')
        # ensure user owns registration - prevents IDOR
        db.session.delete(reg)
        db.session.commit()

    @staticmethod
    def list_user_registrations(user_id: int):
        """List all registrations for a given user."""
        return Registration.query.filter_by(user_id=user_id).all()