import os
from flask import Flask
from src.config import DevelopConfig, ProductionConfig
from src.database.DB import db
from src.OAuth.OAuth import oauth
from src.utils.data_serializers import marshmallow
from src.utils.login_manager import login_manager


if os.environ.get('ENV') == 'PRODUCTION':
    config = ProductionConfig
else:
    config = DevelopConfig
    print('THIS IS DEVELOP SERVER!')

print(os.environ.get('PYTHONUNBUFFERED'))

def create_app(config_name=config):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    oauth.init_app(app)
    marshmallow.init_app(app)
    login_manager.init_app(app)

    from src.product.routes import product
    from src.auth.routes import auth
    from src.cart.routes import cart
    from src.order.routes import order
    from src.auth.google_oauth import google_blueprint
    from src.auth.facebook_oauth import facebook_blueprint

    app.register_blueprint(product)
    app.register_blueprint(auth)
    app.register_blueprint(cart, url_prefix='/cart/')
    app.register_blueprint(order)
    app.register_blueprint(google_blueprint, url_prefix='/google-oauth/')
    app.register_blueprint(facebook_blueprint, url_prefix='/facebook-oauth/')
    return app
