from flask import Blueprint, jsonify, request


order = Blueprint('order', __name__)


@order.get('/order')
def get_order():
    pass


@order.post('/order')
def submit_order():
    pass


@order.delete('/order')
def delete_order():
    pass


@order.get('/completed-order')
def copleted_oderd():
    pass
