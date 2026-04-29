from app.catalog.models.product import Product
from sqlalchemy import or_

def search_products(query):
    if not query:
        return []

    return Product.query.filter(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.generic_name.ilike(f"%{query}%"),
            Product.category.ilike(f"%{query}%")
        )
    ).all()
