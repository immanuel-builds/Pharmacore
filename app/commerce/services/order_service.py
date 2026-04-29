from app.catalog.models.product import db
from app.commerce.models.order import Order, OrderItem
from app.commerce.services.cart_service import get_cart, clear_cart
from app.ops.services.ops_service import reserve_stock

def create_order(user_id):
    cart_items = get_cart(user_id)
    if not cart_items:
        return None

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order(user_id=user_id, total_price=total_price, status='pending')
    db.session.add(order)
    db.session.flush() # Get order.id

    ops_results = []
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            price=item.product.price, # Snapshot price
            quantity=item.quantity
        )
        db.session.add(order_item)

        # Call OPS to reserve
        ops_res = reserve_stock(item.product_id, item.quantity)
        ops_results.append(ops_res)

    db.session.commit()
    clear_cart(user_id)

    # Return order and the most relevant OPS info (e.g. ETA)
    return {
        "order": order,
        "ops": ops_results[0] if ops_results else {}
    }

def get_order_by_id(order_id):
    return Order.query.get(order_id)

def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
    return order
