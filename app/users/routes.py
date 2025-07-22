from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas import UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""
    payload = request.get_json() or {}
    user = UserService.create_user(
        username=payload.get('username'),
        email=payload.get('email'),
        password=payload.get('password')
    )
    return jsonify(user_schema.dump(user)), 201

@users_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return access token."""
    payload = request.get_json() or {}
    token = UserService.authenticate(
        email=payload.get('email'),
        password=payload.get('password')
    )
    return jsonify({'access_token': token}), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Fetch a single user by ID."""
    user = UserService.get_user_by_id(user_id)
    return jsonify(user_schema.dump(user)), 200