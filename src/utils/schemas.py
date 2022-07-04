from flask_marshmallow import Marshmallow
from src.product.models import Product
from src.cart.models import Cart

marshmallow = Marshmallow()


class ProductSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True


class CartSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        include_fk = True
