import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
from app.exceptions import (
    UserValidationError,
    AuthenticationError,
    NotFoundError,
    PermissionError,
)

# global extensions
talisman = Talisman()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config: dict = None) -> Flask:
    """Application factory. Initializes Flask app, extensions, error handlers, and blueprints."""
    app = Flask(__name__)

    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres'
    )  # keep DB credentials in env vars
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)
    app.config['TESTING'] = False
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')
    # secrets pulled from env vars to avoid leaks

    # Override defaults with testing or other config if provided
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    jwt.init_app(app)
    # avoid https redirect errors when developing locally
    # only provide a simple Content-Security-Policy, skip HSTS to avoid
    # certificate requirements in dev or test environments
    talisman.init_app(
        app,
        force_https=False,
        strict_transport_security=False,
        content_security_policy={
            "default-src": [
                "'self'",
                "https://stackpath.bootstrapcdn.com",
                "https://code.jquery.com",
            ]
        },
    )



    # Global error handlers
    @app.errorhandler(UserValidationError)
    def handle_user_validation(error):
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        return jsonify({'error': str(error)}), 401

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({'error': str(error)}), 404

    @app.errorhandler(PermissionError)
    def handle_permission_error(error):
        return jsonify({'error': str(error)}), 403

    # Register blueprints
    from app.users.routes import users_bp
    from app.events.routes import events_bp
    from app.home import home_bp
    from app.registrations.routes import registrations_bp
    from app.frontend.routes import frontend_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(frontend_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app