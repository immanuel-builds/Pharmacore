from flask import Blueprint, jsonify, request
from app.catalog.models.product import Product

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    query = Product.query
    if category:
        query = query.filter_by(category=category)

    products = query.all()
    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in products],
        "error": None
    })

@catalog_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"status": "error", "error": "Product not found"}), 404

    return jsonify({
        "status": "success",
        "data": product.to_dict(),
        "error": None
    })

@catalog_bp.route('/search', methods=['GET'])
def search_products():
    q = request.args.get('q', '')
    products = Product.query.filter(
        (Product.name.ilike(f'%{q}%')) |
        (Product.generic_name.ilike(f'%{q}%')) |
        (Product.category.ilike(f'%{q}%'))
    ).all()

    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in products],
        "error": None
    })
