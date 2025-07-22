from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/dashboard')
@jwt_required()
def dashboard():
    return redirect(url_for('events.get_events'))
