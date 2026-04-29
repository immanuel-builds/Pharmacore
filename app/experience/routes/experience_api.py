from flask import Blueprint, jsonify, request, session
from app.experience.services.aggregator_service import AggregatorService

experience_bp = Blueprint('experience', __name__, url_prefix='/experience')

@experience_bp.route('/product-view/<int:product_id>', methods=['POST'])
def product_view(product_id):
    data = request.get_json() or {}
    user_location = data.get('user_location')
    user_id = session.get('user_id')

    result = AggregatorService.get_full_product_view(product_id, user_id, user_location)
    if not result:
        return jsonify({"status": "error", "error": "Product not found"}), 404

    return jsonify({
        "status": "success",
        "data": result,
        "error": None
    })

@experience_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    result = AggregatorService.get_dashboard(user_id)

    return jsonify({
        "status": "success",
        "data": result,
        "error": None
    })
