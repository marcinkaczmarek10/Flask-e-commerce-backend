from ..database.DB import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    id = db.Column(db.Ineger, primary_key=True)
    username = db.Column(db.Sting(20), unique=True, nullable=False)
    email = db.Column(db.Sting(100), unique=True, nullable=False)
    password = db.Column(db.Sting(60), nullable=False)

    def get_token(self, expires_sec=1800):
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


class Product(db.Model):
    category = db.Column()
    name = db.Column()
    description = db.Column()
    price = db.Column()
    quantity = db.Column()

    def __repr__(self):
        return f'Product({self.name})'
