from app.ops.models.inventory import Inventory
from app.ops.models.reservation import Reservation
from app import db

class InventoryService:
    @staticmethod
    def get_stock(product_id, store_id=None):
        query = Inventory.query.filter_by(product_id=product_id)
        if store_id:
            query = query.filter_by(store_id=store_id)
        return query.all()

    @staticmethod
    def update_stock(store_id, product_id, qty):
        item = Inventory.query.filter_by(store_id=store_id, product_id=product_id).first()
        if item:
            item.stock = qty
        else:
            item = Inventory(store_id=store_id, product_id=product_id, stock=qty)
            db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def check_availability(store_id, product_id, qty):
        inventory = Inventory.query.filter_by(store_id=store_id, product_id=product_id).first()
        if not inventory or inventory.stock < qty:
            return False

        # Also account for active reservations
        reserved = db.session.query(db.func.sum(Reservation.quantity)).filter_by(
            store_id=store_id, product_id=product_id, is_active=True
        ).scalar() or 0

        return (inventory.stock - reserved) >= qty

    @staticmethod
    def reserve_stock(store_id, product_id, qty, order_id=None):
        if not InventoryService.check_availability(store_id, product_id, qty):
            return None

        reservation = Reservation(
            store_id=store_id,
            product_id=product_id,
            quantity=qty,
            order_id=order_id,
            is_active=True
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation

    @staticmethod
    def confirm_reservation(reservation_id):
        res = Reservation.query.get(reservation_id)
        if res and res.is_active:
            inventory = Inventory.query.filter_by(store_id=res.store_id, product_id=res.product_id).first()
            if inventory and inventory.stock >= res.quantity:
                inventory.stock -= res.quantity
                res.is_active = False
                db.session.commit()
                return True
        return False

    @staticmethod
    def release_reservation(reservation_id):
        res = Reservation.query.get(reservation_id)
        if res:
            res.is_active = False
            db.session.commit()
            return True
        return False
