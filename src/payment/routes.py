from flask import Blueprint, url_for, request, jsonify
import stripe
from src.config import Config
import os
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest


payment = Blueprint('payment', __name__)
stripe.api_key = Config.STRIPE_SECRET_KEY
paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID')
paypal_client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')
paypal_env = SandboxEnvironment(client_id=paypal_client_id, client_secret=paypal_client_secret)
paypal_client = PayPalHttpClient(paypal_env)


@payment.post('/stripe-checkout')
def create_stripe_checkout():
    req = request.get_json()
    price = stripe.Price.create(
        product=req['order_name'],
        unit_amount=req['price'],
        currency='pln'
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price.stripe_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('completed_order', _external=True),
            cancel_url=url_for('order', _external=True),
        )
    except Exception as err:
        return jsonify({'message': err}), 400

    return url_for(checkout_session.url, _external=True), 303


@payment.post('/stripe-webhook')
def stripe_webhook():
    event = None
    payload = request.get_json()
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')

    try:
        event = stripe.Event.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as err:
        raise err

    if event is None:
        return jsonify({'message': 'Unhandled event!'}), 400
    return jsonify({'message': 'Success!'}), 200


@payment.post('/paypal-checkout')
def paypal_checkout():
    req = request.get_json()
    paypal_request = OrdersCreateRequest().prefer('return=representation')
    create_request = paypal_request.request_body({
        'intent': 'CAPTURE',
        'purchase_units': [{
            'amount': {
                'currency_code': 'pln',
                'value': req['price']
            }
        }
        ]
    })
    try:
        response = paypal_client.execute(create_request)
        approve_links = [link.result for link in response.result.links]
        return jsonify({'approve_links': approve_links})
    except IOError as err:
        return jsonify({'message': err}), 400


@payment.get('paypal-capturing-order')
def paypal_orders():
    paypal_req = OrdersCaptureRequest('APPROVED-ORDER-ID')
    try:
        resp = paypal_client.execute(paypal_req)
        return jsonify({'paypal_order_id': resp.result.id})
    except IOError as err:
        return jsonify({'message': err})
