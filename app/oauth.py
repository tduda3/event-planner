from flask import Blueprint, url_for, redirect, render_template
from flask_jwt_extended import create_access_token
from app import oauth, db
from app.models import User

oauth_bp = Blueprint('oauth', __name__)

@oauth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('oauth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@oauth_bp.route('/callback')
def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo', token=token)
    user_info = resp.json()
    email = user_info.get('email')
    username = user_info.get('name') or email.split('@')[0]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email, password_hash='')
        db.session.add(user)
        db.session.commit()
    jwt_token = create_access_token(identity=str(user.id))
    return render_template('oauth_callback.html', token=jwt_token)

