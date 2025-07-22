# app/frontend/routes.py
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Event, Registration
from app.services.event_service import EventService

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/home')
def home():
    return render_template('home.html')

@frontend_bp.route('/register')
def register_page():
    return render_template('register.html')

@frontend_bp.route('/login')
def login_page():
    return render_template('login.html')

@frontend_bp.route('/events')
@jwt_required(optional=True)
def events_page():
    # Fetch events and mark attendance
    events = Event.query.order_by(Event.datetime).all()
    user_id = get_jwt_identity()
    attending_ids = set()
    if user_id:
        regs = Registration.query.filter_by(user_id=user_id).all()
        attending_ids = {r.event_id for r in regs}
    # Simplify for template
    simple_events = []
    for e in events:
        simple_events.append({
            'id': e.id,
            'title': e.title,
            'is_attending': (e.id in attending_ids)
        })
    return render_template('events.html', events=simple_events)

@frontend_bp.route('/events/<int:event_id>')
@jwt_required(optional=True)
def event_detail_page(event_id):
    event = EventService.get_event(event_id)
    user_id = get_jwt_identity()
    attending = False
    if user_id and Registration.query.filter_by(user_id=user_id, event_id=event_id).first():
        attending = True
    return render_template(
        'event_detail.html',
        event=event,
        attending=attending
    )