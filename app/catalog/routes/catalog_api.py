from flask import Blueprint, jsonify, request
from app.catalog.services.catalog_service import get_all_products, get_product_by_id
from app.catalog.services.search_service import search_products
from app.catalog.services.view_service import get_product_view

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api/catalog')

@catalog_bp.route('/products', methods=['GET'])
def list_products():
    products = get_all_products()
    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in products],
        "meta": {"total": len(products)},
        "error": None
    })

@catalog_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        return jsonify({
            "status": "success",
            "data": product.to_dict(),
            "meta": {},
            "error": None
        })
    else:
        return jsonify({
            "status": "error",
            "data": None,
            "meta": {},
            "error": "Product not found"
        }), 404

@catalog_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    products = search_products(query)
    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in products],
        "meta": {"query": query, "total": len(products)},
        "error": None
    })

@catalog_bp.route('/product-view/<int:product_id>', methods=['GET'])
def product_view(product_id):
    view_data = get_product_view(product_id)
    if view_data:
        return jsonify({
            "status": "success",
            "data": view_data,
            "meta": {},
            "error": None
        })
    else:
        return jsonify({
            "status": "error",
            "data": None,
            "meta": {},
            "error": "Product not found"
        }), 404
