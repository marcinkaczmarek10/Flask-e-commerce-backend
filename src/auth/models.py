from src.database.DB import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cart_items = db.relationship('Cart', backref='cart')

    def get_token(self, expires_sec=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({
            'user_id': self.id
        }).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            verified_user = serializer.loads(token)['user_id']
        except token is None:
            return None
        return db.session.query(User).get(verified_user)

    def __repr__(self):
        return f'User({self.username}, {self.email})'
