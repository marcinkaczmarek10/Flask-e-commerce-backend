from src.database.DB import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    cart = db.relationship('Cart', backref='cart_item')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref='category')
