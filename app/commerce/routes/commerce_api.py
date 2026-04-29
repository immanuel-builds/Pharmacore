from flask import Blueprint, jsonify, request, session
from app.commerce.services import cart_service, order_service, payment_service

commerce_api = Blueprint('commerce_api', __name__)

def get_current_user():
    return session.get("user_id")

@commerce_api.before_request
def check_auth():
    # Only check auth for API endpoints, not for templates if they were registered here
    # (but they are registered in main.py, so this should only affect /cart GET/POST, etc.)
    if not get_current_user():
        return jsonify({
            "status": "error",
            "data": None,
            "error": "Unauthorized"
        }), 401

@commerce_api.route('/cart', methods=['GET'])
def get_cart():
    user_id = get_current_user()
    items = cart_service.get_cart(user_id)
    return jsonify({
        "status": "success",
        "data": [item.to_dict() for item in items],
        "meta": {"total_items": len(items)},
        "error": None
    })

@commerce_api.route('/cart/add', methods=['POST'])
def add_to_cart():
    user_id = get_current_user()
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({"status": "error", "error": "Product ID required"}), 400

    item = cart_service.add_to_cart(user_id, product_id, quantity)
    return jsonify({
        "status": "success",
        "data": item.to_dict() if item else None,
        "error": None
    })

@commerce_api.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    user_id = get_current_user()
    data = request.json
    product_id = data.get('product_id')

    cart_service.remove_from_cart(user_id, product_id)
    return jsonify({
        "status": "success",
        "data": True,
        "error": None
    })

@commerce_api.route('/order/create', methods=['POST'])
def create_order():
    user_id = get_current_user()
    result = order_service.create_order(user_id)
    if not result:
        return jsonify({"status": "error", "error": "Cart is empty"}), 400

    return jsonify({
        "status": "success",
        "data": {
            "order": result["order"].to_dict(),
            "ops": result["ops"]
        },
        "error": None
    })

@commerce_api.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = order_service.get_order_by_id(order_id)
    if order:
        return jsonify({
            "status": "success",
            "data": order.to_dict(),
            "error": None
        })
    return jsonify({"status": "error", "error": "Order not found"}), 404

@commerce_api.route('/payment/pay', methods=['POST'])
def process_payment():
    data = request.json
    order_id = data.get('order_id')
    if not order_id:
        return jsonify({"status": "error", "error": "Order ID required"}), 400

    success = payment_service.process_payment(order_id)
    return jsonify({
        "status": "success",
        "data": {"success": success},
        "error": None
    })
