import json
from flask import Blueprint, redirect, request, url_for, flash, jsonify
from flask_login import current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from src.models.DB import SessionManager

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user_data = json.loads(request.data)
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

    if user_in_database():
        flash('User created!')
        send_verifiaction_mail(user)
        return redirect(url_for('auth.login'))

    return jsonify({})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


@auth.route('/logout', methods=['POST'])
def logout():
   logout_user()
   return redirect(url_for('home'))


@auth.route('/reset-password', methods=['POST'])
def reset_password_submit():
    if current_user.is_authenticated:
        return redirect('/')
    verified_user = db.session.query(User).filter_by(email=form.email.data).first()
        if verified_user is None:
            flash('no user', 'danger')
        send_reset_password_mail(verified_user)
        flash('Reset link sent to your email', 'success')
        return redirect('/login')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect('/')

    verified_user = User.verify_token(token)
    if not verified_user:
        flash('blank', 'danger')
        return redirect('/reset-password')

    user_data = json.loads(request.data)
    hashed_password = generate_password_hash(
        user_data['password'],
        method='sha256'
    )
    with SessionManager as session:
        user_new_password = {
            User.password: hashed_password
        }
        session.add(user_new_password)
    flash('Password Updated!', 'success')
    return redirect('/login')

