from app.commerce.services.order_service import update_order_status
from app.ops.services.ops_service import confirm_stock_reduction

def process_payment(order_id):
    """
    Mock Payment Service.
    In Phase 2, this will integrate with Razorpay.
    """
    # Logic: If order exists, mark as paid
    update_order_status(order_id, 'paid')

    # Confirm with OPS
    # (Simplified: in real app, we'd fetch order items first)
    confirm_stock_reduction(None, None)

    return True
