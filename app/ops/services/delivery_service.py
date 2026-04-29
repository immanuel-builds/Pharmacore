from app.ops.models.store import Store
from app.ops.services.inventory_service import InventoryService

class DeliveryService:
    @staticmethod
    def calculate_distance(loc1, loc2):
        """
        Simple Euclidean distance: sqrt((lat1-lat2)^2 + (lng1-lng2)^2)
        """
        return ((loc1['lat'] - loc2['lat'])**2 + (loc1['lng'] - loc2['lng'])**2) ** 0.5

    @staticmethod
    def estimate_eta(distance):
        """
        < 0.02 deg (~2 km) -> 10 min
        < 0.05 deg (~5 km) -> 20 min
        > 0.05 deg -> 30 min
        Note: Degrees to km conversion is roughly 1 deg approx 111 km.
        0.02 deg is approx 2.2 km.
        """
        # Using degrees directly for simplicity in the formula as per directive
        if distance < 0.02:
            return "10 mins"
        elif distance < 0.05:
            return "20 mins"
        else:
            return "30 mins"

    @staticmethod
    def assign_store(user_location, items):
        """
        Find nearest store that is active, within radius, and has stock for all items.
        items: list of {'product_id': id, 'quantity': qty}
        """
        active_stores = Store.query.filter_by(is_active=True).all()
        eligible_stores = []

        for store in active_stores:
            store_loc = {"lat": store.location_lat, "lng": store.location_lng}
            dist = DeliveryService.calculate_distance(user_location, store_loc)

            # Directive: if distance > store.radius_km -> NOT eligible
            # Converting radius_km to approximate degrees for comparison: 1km approx 0.009 deg
            radius_deg = store.radius_km * 0.009

            if dist <= radius_deg:
                # Check stock for all items
                all_items_available = True
                for item in items:
                    if not InventoryService.check_availability(store.id, item['product_id'], item['quantity']):
                        all_items_available = False
                        break

                if all_items_available:
                    eligible_stores.append({
                        "store": store,
                        "distance": dist
                    })

        if not eligible_stores:
            return None

        # Sort by distance and pick nearest
        eligible_stores.sort(key=lambda x: x["distance"])
        best_match = eligible_stores[0]

        return {
            "store": best_match["store"],
            "distance": best_match["distance"],
            "eta": DeliveryService.estimate_eta(best_match["distance"])
        }
