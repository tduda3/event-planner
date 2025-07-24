from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Event, Registration
from app.services.event_service import EventService
from app.services.user_service import UserService

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/home')
def home():
    """Render the home page."""
    return render_template('home.html')

@frontend_bp.route('/register')
def register_page():
    """Show the registration page."""
    return render_template('register.html')

@frontend_bp.route('/login')
def login_page():
    """Show the login page."""
    return render_template('login.html')

@frontend_bp.route('/events')
@jwt_required(optional=True)
def events_page():
    """Display a list of events for the user."""
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    filters = {}
    if search:
        filters['search'] = search

    pagination = EventService.list_events(filters, page, per_page)
    events = pagination.items

    user_id = get_jwt_identity()
    attending_ids = set()
    if user_id:
        regs = Registration.query.filter_by(user_id=user_id).all()
        attending_ids = {r.event_id for r in regs}

    simple_events = [
        {
            'id': e.id,
            'title': e.title,
            'attendee_count': len(e.registrations),
            'is_attending': e.id in attending_ids,
        }
        for e in events
    ]

    return render_template(
        'events.html',
        events=simple_events,
        search=search,
        page=pagination.page,
        per_page=pagination.per_page,
        has_next=pagination.has_next,
        has_prev=pagination.has_prev,
    )

@frontend_bp.route('/events/<int:event_id>')
@jwt_required(optional=True)
def event_detail_page(event_id):
    """Show details for a single event."""
    event = EventService.get_event(event_id)
    user_id = get_jwt_identity()
    attending = False
    if user_id and Registration.query.filter_by(user_id=user_id, event_id=event_id).first():
        attending = True
    attendee_count = len(event.registrations)
    is_owner = user_id is not None and int(user_id) == event.owner_id
    return render_template(
        'event_detail.html',
        event=event,
        attending=attending,
        is_owner=is_owner,
        attendee_count=attendee_count
    )


@frontend_bp.route('/users/<int:user_id>')
def user_profile_page(user_id):
    """Render a user's profile page."""
    user = UserService.get_user_by_id(user_id)
    created = Event.query.filter_by(owner_id=user_id).order_by(Event.datetime).all()
    attending = (
        Event.query.join(Registration)
        .filter(Registration.user_id == user_id)
        .order_by(Event.datetime)
        .all()
    )
    return render_template(
        'profile.html',
        user=user,
        created=created,
        attending=attending,
    )
