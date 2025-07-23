from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app import db
from app.exceptions import UserValidationError, AuthenticationError, NotFoundError

class UserService:
    """Service layer for user-related operations."""

    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        """Create a new user after validating inputs."""
        if not username or not email or not password:
            raise UserValidationError('Username, email, and password are required')
        if '@' not in email:
            raise UserValidationError('Invalid email address')
        #Enforce basic strong password practices
        if len(password) < 8:
            raise UserValidationError('Password must be at least 8 characters')
        # Check for existing user
        if User.query.filter((User.username == username) | (User.email == email)).first():
            raise UserValidationError('User with that username or email already exists')
        # SQLAlchemy parameter binding thwarts SQL injection
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate(email: str, password: str) -> str:
        """Authenticate a user and return a JWT access token."""
        if not email or not password:
            raise AuthenticationError('Email and password are required')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            raise AuthenticationError('Invalid credentials')
        token = create_access_token(identity=str(user.id))
        return token

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Retrieve a user by their ID."""
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(f'User with id {user_id} not found')
        return user