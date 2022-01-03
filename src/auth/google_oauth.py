from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from src.auth.models import OAuth, User
from flask_login import login_user
from src.database.DB import db, SessionManager
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from flask import jsonify


google_blueprint = make_google_blueprint(scope=["profile", "email"],
                                         storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
                                         )


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        return jsonify({'message': 'Could not authorize!'}), 401
    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        return jsonify({'message': 'Could not authorize!'}), 401

    account_info = resp.json()
    query = OAuth.query.filter_by(provider=blueprint.name, user_id=account_info['id'])
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, user_id=account_info['id'], token=token)

    if oauth.user:
        login_user(oauth.user)
        return jsonify({}), 200
    else:
        user = User(email=account_info['email'])
        oauth.user = user

        with SessionManager() as session:
            session.add(user)
            session.add(oauth)
        return jsonify({}), 200


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    resp = f'Something went wrong with oauth! You{blueprint.name}, got message:{message}, and response{response}'
    return jsonify({'message': resp})
