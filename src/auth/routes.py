import json
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.auth.models import User
from src.database.DB import SessionManager, db


auth = Blueprint('auth', __name__)


@auth.post('/register')
def register():
    user_data = request.get_json()
    print(user_data)
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


@auth.get('/login')
def login():
    auth_header = request.authorization

    if not auth_header or not auth_header.username or not auth_header.password:
        return jsonify({'message': 'Could not verify!'}), 401

    user = User.query.filter_by(username=auth_header.username).first()

    if user and check_password_hash(user.password, auth_header.password):
        token = user.get_token()
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Wrong password'}), 401
