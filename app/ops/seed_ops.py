from app import create_app, db
from app.ops.models.store import Store
from app.ops.models.inventory import Inventory

def load_ops_seed():
    app = create_app()
    with app.app_context():
        # Clear existing
        db.session.query(Inventory).delete()
        db.session.query(Store).delete()

        # Stores
        # Store A (Central) - lat: 12.9716, lng: 77.5946, radius_km: 5
        # Store B (South) - lat: 12.9352, lng: 77.6245, radius_km: 5
        s1 = Store(name="Store A", location_lat=12.9716, location_lng=77.5946, radius_km=5)
        s2 = Store(name="Store B", location_lat=12.9352, location_lng=77.6245, radius_km=5)
        db.session.add_all([s1, s2])
        db.session.commit()

        # Inventory
        # Product IDs 1: Paracetamol, 2: Ibuprofen, 3: Aspirin
        inventory_data = [
            {"store_id": s1.id, "product_id": 1, "stock": 50},
            {"store_id": s1.id, "product_id": 2, "stock": 30},
            {"store_id": s1.id, "product_id": 3, "stock": 10},
            {"store_id": s2.id, "product_id": 1, "stock": 20},
            {"store_id": s2.id, "product_id": 4, "stock": 15}, # Morphine placeholder
        ]

        for item in inventory_data:
            inv = Inventory(store_id=item['store_id'], product_id=item['product_id'], stock=item['stock'])
            db.session.add(inv)

        db.session.commit()
        print("OPS seed data loaded successfully.")

if __name__ == "__main__":
    load_ops_seed()
