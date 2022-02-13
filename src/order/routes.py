from flask import Blueprint, jsonify, request
from flask_login import current_user
from src.database.DB import SessionManager


order = Blueprint('order', __name__)


@order.get('/order')
def get_order():
    user = current_user
    if user.is_authenticated:
        # handle authenticated user order

        with SessionManager() as session:
            # add order to DB
            pass
    else:
        pass
        # handle unauthenticated user order
    return jsonify({})


@order.post('/order')
def submit_order():
    if current_user.is_authenticated:
        pass
    return jsonify({})


@order.delete('/order')
def delete_order():
    if current_user.is_authenticated:
        pass
    return jsonify({})


@order.get('/completed-order')
def completed_order():
    if current_user.is_authenticated:
        pass
    return jsonify({})
