from app.models import Event
from app import db
from app.exceptions import NotFoundError, UserValidationError, PermissionError
from datetime import datetime
from sqlalchemy import or_

class EventService:
    """Service layer for event management."""

    @staticmethod
    def create_event(owner_id: int, data: dict) -> Event:
        """Validate and create a new event."""
        title = data.get('title')
        event_datetime = data.get('datetime')
        location = data.get('location')
        description = data.get('description')

        if not title or not event_datetime or not location:
            raise UserValidationError('Title, datetime, and location are required')
        try:
            dt = datetime.fromisoformat(event_datetime)
        except ValueError:
            raise UserValidationError('Invalid datetime format')

        new_event = Event(
            title=title,
            datetime=dt,
            location=location,
            description=description,
            owner_id=owner_id
        )
        db.session.add(new_event)
        # Commit so event is immediately available to queries
        db.session.commit()
        return new_event

    @staticmethod
    def get_event(event_id: int) -> Event:
        """Retrieve an event by its ID."""
        event = Event.query.get(event_id)
        if not event:
            raise NotFoundError(f'Event with id {event_id} not found')
        return event

    @staticmethod
    def update_event(event_id: int, owner_id: int, data: dict) -> Event:
        """Update an existing event if owned by user."""
        event = EventService.get_event(event_id)
        if event.owner_id != owner_id:
            raise PermissionError('You do not have permission to update this event')
        # ensure only owner can modify to avoid IDOR

        if 'title' in data:
            event.title = data['title']

        #datetime required
        if 'datetime' in data:
            try:
                event.datetime = datetime.fromisoformat(data['datetime'])
            except ValueError:
                raise UserValidationError('Invalid datetime format')
        if 'location' in data:
            event.location = data['location']
        if 'description' in data:
            event.description = data['description']

        db.session.commit()
        return event

    @staticmethod
    def delete_event(event_id: int, owner_id: int) -> None:
        """Delete an event if owned by user."""
        event = EventService.get_event(event_id)
        if event.owner_id != owner_id:
            raise PermissionError('You do not have permission to delete this event')
        # avoid IDOR by verifying ownership before delete
        db.session.delete(event)
        db.session.commit()

    @staticmethod
    def list_events(filters: dict = None, page: int = 1, per_page: int = 20):
        """Return paginated list of events."""
        query = Event.query  # ORM escapes inputs to prevent SQL injection
        if filters:
            owner = filters.get('owner_id')
            if owner:
                query = query.filter_by(owner_id=owner)
            date_str = filters.get('date')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str).date()
                    query = query.filter(db.func.date(Event.datetime) == date_obj)
                except ValueError:
                    raise UserValidationError('Invalid date format, expected ISO 8601 string')
            search = filters.get('search')
            if search:
                like = f"%{search}%"
                query = query.filter(or_(Event.title.ilike(like), Event.description.ilike(like)))
        return query.order_by(Event.datetime).paginate(page=page, per_page=per_page)

    @staticmethod
    def event_to_ics(event: Event) -> str:
        """Return an iCalendar representation of an event."""
        now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        start = event.datetime.strftime('%Y%m%dT%H%M%SZ')
        lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'BEGIN:VEVENT',
            f'UID:{event.id}@event-planner',
            f'DTSTAMP:{now}',
            f'DTSTART:{start}',
            f'SUMMARY:{event.title}',
            f'DESCRIPTION:{event.description or ""}',
            f'LOCATION:{event.location}',
            'END:VEVENT',
            'END:VCALENDAR',
        ]
        return '\r\n'.join(lines) + '\r\n'
