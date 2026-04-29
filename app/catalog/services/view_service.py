from app.catalog.services.catalog_service import get_product_by_id
from app.catalog.services.core_client import analyze_interactions

def get_product_view(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return None

    # Call CORE module mock
    safety_data = analyze_interactions([product.generic_name])

    return {
        "product": product.to_dict(),
        "safety": safety_data
    }
