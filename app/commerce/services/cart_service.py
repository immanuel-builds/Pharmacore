from app.catalog.models.product import db
from app.commerce.models.cart import CartItem

def add_to_cart(user_id, product_id, qty=1):
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=qty)
        db.session.add(item)

    if item.quantity <= 0:
        db.session.delete(item)

    db.session.commit()
    return item

def remove_from_cart(user_id, product_id):
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return True

def get_cart(user_id):
    return CartItem.query.filter_by(user_id=user_id).all()

def clear_cart(user_id):
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
