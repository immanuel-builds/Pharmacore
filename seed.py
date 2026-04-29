from app import create_app, db
from app.core.ingestion.seed_loader import load_seed_data
from app.ops.seed_ops import load_ops_seed
from app.catalog.models.product import Product
import os

def run_seed():
    app = create_app()
    with app.app_context():
        # Core & Ops seeds
        core_seed_path = os.path.join(app.root_path, 'core/ingestion/data/seed.json')
        load_seed_data(core_seed_path)
        load_ops_seed()

        # Catalog seed
        if not Product.query.first():
            products = [
                Product(
                    name="Crocin 500mg",
                    generic_name="Paracetamol",
                    dosage="500mg",
                    form="Tablet",
                    category="Pain Relief",
                    price=15.5,
                    stock=100,
                    description="Common pain reliever and fever reducer.",
                    usage="Take 1-2 tablets every 4-6 hours.",
                    warnings="Do not exceed 4g per day.",
                    confidence=0.95,
                    source="DrugBank"
                ),
                Product(
                    name="Advil 200mg",
                    generic_name="Ibuprofen",
                    dosage="200mg",
                    form="Capsule",
                    category="Pain Relief",
                    price=25.0,
                    stock=50,
                    description="Nonsteroidal anti-inflammatory drug (NSAID).",
                    usage="Take 1 capsule every 4-6 hours.",
                    warnings="May cause stomach bleeding.",
                    confidence=0.92,
                    source="PubChem"
                )
            ]
            db.session.add_all(products)
            db.session.commit()
            print("Catalog seed data loaded.")

        print("Integrated seeding complete.")

if __name__ == "__main__":
    run_seed()
