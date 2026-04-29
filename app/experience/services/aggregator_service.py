from app.catalog.models.product import Product
from app.core.services.interaction_service import InteractionService
from app.ops.services.delivery_service import DeliveryService
from app.commerce.models.commerce import CartItem
from app import db

class AggregatorService:
    @staticmethod
    def get_full_product_view(product_id, user_id=None, user_location=None):
        """
        Aggregates product info, safety (CORE), availability (OPS), and cart state.
        """
        product = Product.query.get(product_id)
        if not product:
            return None

        # 1. Safety Info (CORE)
        safety_info = None
        if product.generic_name:
            # For a single product, we just check its own profile
            # but usually interactions are between substances.
            # Here we might return its mechanism and clinical mapping.
            from app.core.models.substance import Substance
            substance = Substance.query.filter_by(name=product.generic_name).first()
            if substance:
                safety_info = {
                    "mechanism": substance.mechanism,
                    "confidence": substance.confidence,
                    "source": substance.source,
                    "risk_level": "Minimal" if not product.prescription_required else "Moderate"
                }

        # 2. Availability (OPS)
        delivery_info = None
        if user_location:
            items = [{"product_id": product.id, "quantity": 1}]
            assignment = DeliveryService.assign_store(user_location, items)
            if assignment:
                delivery_info = {
                    "available": True,
                    "store": assignment['store'].name,
                    "eta": assignment['eta']
                }
            else:
                delivery_info = {
                    "available": False,
                    "error": "No coverage in your area"
                }

        # 3. Cart State
        in_cart = False
        if user_id:
            cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
            in_cart = cart_item is not None

        return {
            "product": product.to_dict(),
            "safety": safety_info,
            "delivery": delivery_info,
            "in_cart": in_cart
        }

    @staticmethod
    def get_dashboard(user_id=None):
        """
        Aggregates data for the home/dashboard view.
        """
        # Feature products
        featured_products = Product.query.limit(5).all()

        # In a real app, this might include user's recent orders,
        # personalized recommendations, etc.

        return {
            "featured_products": [p.to_dict() for p in featured_products],
            "categories": ["Pain Relief", "Opioid Analgesic", "SSRI", "Stimulant"]
        }
