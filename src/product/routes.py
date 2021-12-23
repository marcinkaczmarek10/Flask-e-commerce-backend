import json
from flask import Blueprint, jsonify, request
from src.database.DB import SessionManager
from src.product.models import Product, Category
from src.utils.data_serializers import ProductSchema


product = Blueprint('product', __name__)


@product.get('/products')
def list_all_products():
    query = Product.query.all()
    schema = ProductSchema(many=True)
    products = schema.dump(query)

    return jsonify(products), 200


@product.get('/products/<category>')
def list_products_by_category(category):
    query = Product.query.filter_by(category_id=category).all()
    schema = ProductSchema(many=True)
    products = schema.dump(query)

    return jsonify(products), 200


@product.get('/product/<product_id>')
def product_detail(product_id):
    query = Product.query.filter_by(id=product_id).first()
    schema = ProductSchema()
    products = schema.dump(query)

    return jsonify(products), 200


@product.post('/category')
def create_category():
    req = request.get_json()
    category = Category(
        name=req['name']
    )
    category_exist = Category.query.filter_by(name=req['name']).first()
    if req and not category_exist:
        with SessionManager() as session:
            session.add(category)

        return jsonify({'message': 'Category created!'}), 200
    if category_exist:
        return jsonify({'message': 'Category already exist!'}), 403
    return jsonify({'message': 'There is no category!'}), 403


@product.delete('/category')
def delete_category():
    req = request.get_json()
    category = Category.query.filter_by(name=req['name']).first()
    if req and category:
        with SessionManager() as session:
            session.delete(category)

        return jsonify({'message': 'Category deleted!'}), 200
    return jsonify({'message': 'There is no category to delete!'}), 403


@product.put('/category')
def update_category():
    pass


@product.post('/product')
def create_product():
    product_request = request.get_json()
    product_to_add = Product(
        name=product_request['name'],
        description=product_request['description'],
        price=product_request['price'],
        category_id=product_request['category']
    )
    with SessionManager() as session:
        session.add(product_to_add)
    return jsonify({'message': 'product added!'}), 200


@product.delete('/product/<product_id>')
def delete_product(product_id):
    pass


@product.put('/product/<product_id>')
def update_product(product_id):
    pass
