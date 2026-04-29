from flask import Blueprint, request, jsonify, session
from app.commerce.models.commerce import CartItem, Order, OrderItem
from app.catalog.models.product import Product
from app.ops.services.delivery_service import DeliveryService
from app.ops.services.inventory_service import InventoryService
from app import db

commerce_bp = Blueprint('commerce', __name__, url_prefix='/commerce')

@commerce_bp.route('/cart', methods=['GET'])
def get_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "error": "Not authenticated"}), 401

    items = CartItem.query.filter_by(user_id=user_id).all()
    data = []
    for item in items:
        p_dict = item.product.to_dict()
        p_dict['quantity'] = item.quantity
        data.append(p_dict)

    return jsonify({"status": "success", "data": data, "error": None})

@commerce_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "error": "Not authenticated"}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    return jsonify({"status": "success", "data": None, "error": None})

@commerce_bp.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "error": "Not authenticated"}), 401

    data = request.get_json()
    user_location = data.get('user_location')

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"status": "error", "error": "Cart is empty"}), 400

    # Prep items for OPS
    items_for_ops = [{"product_id": ci.product_id, "quantity": ci.quantity} for ci in cart_items]

    # 1. OPS assigns store & creates reservations
    assignment = DeliveryService.assign_store(user_location, items_for_ops)
    if not assignment:
        return jsonify({"status": "error", "error": "No store available for delivery"}), 404

    store = assignment['store']

    # 2. Create reservations
    reservation_ids = []
    for item in items_for_ops:
        res = InventoryService.reserve_stock(store.id, item['product_id'], item['quantity'])
        if res:
            reservation_ids.append(res.id)
        else:
            for r_id in reservation_ids:
                InventoryService.release_reservation(r_id)
            return jsonify({"status": "error", "error": "Inventory changed, checkout failed"}), 500

    # 3. Create Order
    total_amount = sum(ci.product.price * ci.quantity for ci in cart_items)
    order = Order(user_id=user_id, store_id=store.id, total_amount=total_amount, status='pending')
    db.session.add(order)
    db.session.flush()

    for ci in cart_items:
        oi = OrderItem(order_id=order.id, product_id=ci.product_id, quantity=ci.quantity, price_at_purchase=ci.product.price)
        db.session.add(oi)
        db.session.delete(ci) # Clear cart

    db.session.commit()

    return jsonify({
        "status": "success",
        "data": {
            "order_id": order.id,
            "total_amount": total_amount,
            "store": store.name,
            "eta": assignment['eta'],
            "reservation_ids": reservation_ids
        },
        "error": None
    })

@commerce_bp.route('/order/<int:order_id>/pay', methods=['POST'])
def pay_order(order_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "error": "Not authenticated"}), 401

    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return jsonify({"status": "error", "error": "Order not found"}), 404

    data = request.get_json()
    reservation_ids = data.get('reservation_ids', [])

    # Mock payment success
    order.status = 'paid'

    # Confirm reservations in OPS
    for r_id in reservation_ids:
        InventoryService.confirm_reservation(r_id)

    db.session.commit()
    return jsonify({"status": "success", "data": {"status": order.status}, "error": None})
