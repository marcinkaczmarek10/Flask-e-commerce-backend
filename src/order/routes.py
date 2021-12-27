from flask import Blueprint, jsonify, request


order = Blueprint('order', __name__)


@order.get('/order')
def get_order():
    pass


@order.post('/order')
def post_order():
    pass
