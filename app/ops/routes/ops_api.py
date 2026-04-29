from flask import Blueprint, jsonify, request
from app.ops.services.inventory_service import InventoryService
from app.ops.services.delivery_service import DeliveryService

ops_bp = Blueprint('ops', __name__, url_prefix='/ops')

@ops_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "module": "delivery-inventory"})

@ops_bp.route('/inventory/<int:product_id>', methods=['GET'])
def get_inventory(product_id):
    results = InventoryService.get_stock(product_id)
    data = [{
        "store_id": item.store_id,
        "store_name": item.store.name,
        "stock": item.stock
    } for item in results]

    return jsonify({
        "status": "success",
        "data": data,
        "error": None
    })

@ops_bp.route('/inventory/update', methods=['POST'])
def update_inventory():
    data = request.get_json()
    store_id = data.get('store_id')
    product_id = data.get('product_id')
    qty = data.get('quantity')

    if not all([store_id, product_id, qty is not None]):
        return jsonify({"status": "error", "error": "Missing required fields"}), 400

    item = InventoryService.update_stock(store_id, product_id, qty)
    return jsonify({
        "status": "success",
        "data": {"store_id": item.store_id, "product_id": item.product_id, "stock": item.stock},
        "error": None
    })

@ops_bp.route('/delivery/assign', methods=['POST'])
def assign_delivery():
    data = request.get_json()
    user_location = data.get('user_location') # {"lat": ..., "lng": ...}
    items = data.get('items') # [{"product_id": ..., "quantity": ...}]

    if not user_location or not items:
        return jsonify({"status": "error", "error": "Missing location or items"}), 400

    assignment = DeliveryService.assign_store(user_location, items)
    if not assignment:
        return jsonify({
            "status": "error",
            "data": None,
            "error": "No store available in your area"
        }), 404

    # Create reservations for all items
    reservations = []
    store = assignment['store']
    for item in items:
        res = InventoryService.reserve_stock(store.id, item['product_id'], item['quantity'])
        if res:
            reservations.append(res.id)
        else:
            # This shouldn't happen if assign_store was correct, but safety first
            # If one fails, we should ideally rollback others
            for r_id in reservations:
                InventoryService.release_reservation(r_id)
            return jsonify({"status": "error", "error": "Inventory changed, assignment failed"}), 500

    return jsonify({
        "status": "success",
        "data": {
            "store": store.name,
            "store_id": store.id,
            "eta": assignment['eta'],
            "distance": round(assignment['distance'], 4),
            "reservations": reservations
        },
        "error": None
    })

@ops_bp.route('/delivery/estimate', methods=['POST'])
def estimate_delivery():
    data = request.get_json()
    user_location = data.get('user_location')
    store_id = data.get('store_id')

    from app.ops.models.store import Store
    store = Store.query.get(store_id)
    if not store:
        return jsonify({"status": "error", "error": "Store not found"}), 404

    store_loc = {"lat": store.location_lat, "lng": store.location_lng}
    dist = DeliveryService.calculate_distance(user_location, store_loc)
    eta = DeliveryService.estimate_eta(dist)

    return jsonify({
        "status": "success",
        "data": {
            "eta": eta,
            "distance": round(dist, 4)
        },
        "error": None
    })

@ops_bp.route('/reservation/confirm', methods=['POST'])
def confirm_reservation():
    data = request.get_json()
    reservation_ids = data.get('reservation_ids', [])

    success_count = 0
    for r_id in reservation_ids:
        if InventoryService.confirm_reservation(r_id):
            success_count += 1

    return jsonify({
        "status": "success",
        "data": {"confirmed_count": success_count},
        "error": None
    })
