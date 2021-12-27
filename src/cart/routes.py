import json
from flask import Blueprint, jsonify, request, session, make_response
from src.cart.models import Cart
from src.auth.models import User
from src.database.DB import SessionManager
from src.utils.data_serializers import CartSchema


cart = Blueprint('cart', __name__)


@cart.post('/add-item<product_id>')
def add_item_to_cart(product_id):
    user = User.query.filter_by(username=session['username']).first()
    if user:
        check_is_item_in_cart = Cart.query.filter_by(product_id=product_id, username=user.username).first()
        if check_is_item_in_cart:
            with SessionManager():
                Cart.query.filter_by(product_id=product_id, username=user.username).\
                    update(quantity=check_is_item_in_cart.quantity+1)
            return jsonify({'message': 'Cart quantity updated!'}), 200

        cart_item = Cart(
            product_id=product_id,
            quantity=1,
            user_id=1
        )
        with SessionManager() as sessionCM:
            sessionCM.add(cart_item)
        return jsonify({'message': 'Item added to cart!'}), 200
    resp = make_response({'message': 'Cart in session'})
    user_cart = json.dumps({
        'product_id': product_id,
        'quantity': 1
    })
    resp.set_cookie('cart',
                    user_cart)
    return resp


@cart.get('/items')
def get_cart_item():
    req = request.headers.get('user_id')
    cart_in_session = session.get('cart')
    if req:
        query = Cart.query.filter_by(user_id=req).all()
        schema = CartSchema(many=True)
        result = json.dumps(schema.dump(query))
        return jsonify(result), 200
    return cart_in_session


@cart.delete('/delete-item<product_id>')
def delete_item_from_cart(product_id):
    product_to_delete = Cart.query.filter_by(product_id=product_id).first()
    if product_to_delete:
        with SessionManager() as sessionCM:
            sessionCM.delete(product_to_delete)
        return jsonify({'message': 'Product deleted from cart!'}), 200
    return jsonify({'message': 'Could not find product!'}), 404


@cart.get('/cookie')
def get_cookie():
    cookie = request.cookies.get('session')
    print(cookie)
    return jsonify(cookie), 200
