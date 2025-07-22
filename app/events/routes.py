from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.event_service import EventService
from app.schemas import EventSchema

events_bp = Blueprint('events', __name__, url_prefix='/api/events')

event_schema = EventSchema()
events_schema = EventSchema(many=True)

@events_bp.route('/', methods=['GET'])
def list_events():
    """List events with optional filtering and pagination."""
    filters = request.args.to_dict()
    page = int(filters.pop('page', 1))
    per_page = int(filters.pop('per_page', 20))
    pagination = EventService.list_events(filters, page, per_page)
    return jsonify({
        'events': events_schema.dump(pagination.items),
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page
    }), 200

@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id: int):
    """Retrieve a single event by ID."""
    event = EventService.get_event(event_id)
    return jsonify(event_schema.dump(event)), 200

@events_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    """Create a new event owned by the current user."""
    data = request.get_json() or {}
    user_id = int(get_jwt_identity())
    event = EventService.create_event(user_id, data)
    return jsonify(event_schema.dump(event)), 201

@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id: int):
    """Update an existing event if owned by user."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    event = EventService.update_event(event_id, user_id, data)
    return jsonify(event_schema.dump(event)), 200

@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id: int):
    """Delete an event if owned by user."""
    user_id = int(get_jwt_identity())
    EventService.delete_event(event_id, user_id)
    return jsonify({'message': 'Event deleted'}), 200