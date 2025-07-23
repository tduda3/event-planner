from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.registration_service import RegistrationService
from app.schemas import RegistrationSchema

registrations_bp = Blueprint('registrations', __name__, url_prefix='/api')
reg_schema = RegistrationSchema()
regs_schema = RegistrationSchema(many=True)

@registrations_bp.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_event(event_id: int):
    """RSVP current user to an event."""
    user_id = int(get_jwt_identity())
    reg = RegistrationService.register_for_event(user_id, event_id)
    return jsonify(reg_schema.dump(reg)), 201

@registrations_bp.route('/registrations/<int:registration_id>', methods=['DELETE'])
@jwt_required()
def cancel_registration(registration_id: int):
    """Cancel a registration."""
    user_id = int(get_jwt_identity())
    RegistrationService.cancel_registration(registration_id, user_id)
    return jsonify({'message': 'Registration canceled'}), 200

@registrations_bp.route('/users/<int:user_id>/registrations', methods=['GET'])
@jwt_required()
def list_registrations(user_id: int):
    """List registrations for a user."""
    regs = RegistrationService.list_user_registrations(user_id)
    return jsonify(regs_schema.dump(regs)), 200
