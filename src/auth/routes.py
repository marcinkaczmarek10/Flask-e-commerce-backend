from flask_login import login_user, logout_user, current_user
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from src.auth.models import User
from src.database.DB import SessionManager
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    user_data = request.get_json()
    user_in_database = User.query.\
        filter_by(username=user_data['username'], email=user_data['email']).first()
    if user_data and not user_in_database:
        hashed_password = generate_password_hash(
            user_data['password'],
            method='sha256'
        )
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password=hashed_password
        )
        with SessionManager() as session:
            session.add(user)

        return jsonify({'message': 'User created!'}), 200
    if user_in_database:
        return jsonify({'message': 'User already exist'}), 403

    return jsonify({'message': 'No data'}), 404


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if google:
        redirect(url_for('google.login'))
    if facebook:
        redirect(url_for('facebook.login'))
    req = request.get_json()
    if not req:
        return jsonify({'message': 'Could not verify!'}), 401

    try:
        user = User.query.filter_by(username=req['email']).first()
    except KeyError:
        return jsonify({'message': 'Bad request!'}), 400

    if user and check_password_hash(user.password, req['password']):
        login_user(user, remember=req['remember'])
        redirect_page = request.args.get('next')
        return redirect(redirect_page) if redirect_page else jsonify({'You have been logged in': 'message'}), 200

    return jsonify({'message': 'Wrong password'}), 401


@auth.get('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'User logged out!'}), 200
