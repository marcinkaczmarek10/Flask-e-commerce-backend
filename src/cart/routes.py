import json
from flask import Blueprint, jsonify, request, make_response, render_template
from src.cart.models import Cart
from src.database.DB import SessionManager
from src.utils.data_serializers import CartSchema


cart = Blueprint('cart', __name__)


@cart.post('/add-item/<product_id>')
def add_item_to_cart(product_id):
    user = request.headers.get('user_id')
    if user:
        check_is_item_in_cart = Cart.query.filter_by(product_id=product_id, user_id=user).first()
        if check_is_item_in_cart:
            with SessionManager():
                Cart.query.filter_by(product_id=product_id, user_id=user).\
                    update(quantity=check_is_item_in_cart.quantity+1)
            return jsonify({'message': 'Cart quantity updated!'}), 200

        cart_item = Cart(
            product_id=product_id,
            quantity=1,
            user_id=user
        )
        with SessionManager() as sessionCM:
            sessionCM.add(cart_item)
        return jsonify({'message': 'Item added to cart!'}), 200
    resp = make_response({'message': 'Cart in session'})
    cart_session = json.loads(request.cookies.get('cart'))
    if cart_session['product_id'] == product_id:
        user_cart = json.dumps({
            'product_id': product_id,
            'quantity': cart_session['quantity']+1
        })
        resp.set_cookie('cart',
                        user_cart,
                        secure=True,
                        samesite='Lax')
        return resp
    user_cart = json.dumps({
        'product_id': product_id,
        'quantity': 1
    })
    resp.set_cookie('cart',
                    user_cart,
                    secure=True,
                    samesite='Lax')
    return resp


@cart.get('/items')
def get_cart_item():
    user = request.headers.get('user_id')
    cart_in_session = request.cookies.get('cart')
    if user:
        query = Cart.query.filter_by(user_id=user).all()
        schema = CartSchema(many=True)
        result = json.dumps(schema.dump(query))
        return jsonify(result), 200
    return cart_in_session if cart_in_session else {'message': 'No cart items'}


@cart.delete('/delete-item/<product_id>')
def delete_item_from_cart(product_id):
    user = request.headers.get('user_id')
    cart_in_session = request.cookies.get('cart')
    if user:
        product_to_delete = Cart.query.filter_by(product_id=product_id, user_id=user).first()
        if product_to_delete:
            with SessionManager() as sessionCM:
                sessionCM.delete(product_to_delete)
            return jsonify({'message': 'Product deleted from cart!'}), 200
        return jsonify({'message': 'Could not find product!'}), 404
    if cart_in_session:
        resp = make_response({'message': 'Cookie deleted!'})
        resp.delete_cookie('cart', secure=True, httponly=True, samesite='Lax')
        return resp
    return jsonify({'message': 'Could not find product!'}), 404


@cart.get('/get')
def dummy_post():
    return render_template('dummy.html')
