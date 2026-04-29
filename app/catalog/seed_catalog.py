from app import create_app, db
from app.catalog.models.product import Product

def load_catalog_seed():
    app = create_app()
    with app.app_context():
        # Clear existing
        db.session.query(Product).delete()

        products = [
            {
                "id": 1,
                "name": "Panadol Extra",
                "generic_name": "Paracetamol",
                "dosage": "500mg",
                "form": "Tablet",
                "category": "Pain Relief",
                "price": 10.50,
                "description": "Effective pain relief for headaches and fever.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDKf77ViqqAHLc9rh9k9kQZnf_l1Bw0-u6GpgB8fFC3tMLcIbTvZ1SwtK_OLRFyIBAGFUDRm57AmWz2iOz4tVyYKA1Bc0i3UsX8O2976l66IUtlCKPD6P-cQJ_1NyS9QUsxMNZxV1Pgh0gTDtIgJ62-4jydSdQBQhvCD0eUcanMXXaAfigTLfVfvFm0kyeDnRypsbNJQ4gDqJfsCKaPpyyfbvuZPa_lc8fdV07PG8zOHKQkaomjRfmiqJZ_o-BoFOIz14tvExA331Y"
            },
            {
                "id": 2,
                "name": "Advil Liquid Gels",
                "generic_name": "Ibuprofen",
                "dosage": "200mg",
                "form": "Liquid Gel",
                "category": "Pain Relief",
                "price": 12.99,
                "description": "Fast-acting relief for joint pain and inflammation.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDLYMym9Xd2gAoTs4C-Ckm_6tibo5KOx_oSj-RYf6L4BOGqqHQ9Yuv6BdGovxOXTXHslU2tolVzXukdb4cwd8TjrrC-G4Dh8LP_d7XupDjnh4-8WYKyiQsxbT2fm9t7rwA02Okzzij4UF7L4aayGplxeK9LBBzZP69bsZLcIKOQilKTxLTZrIHka46dOpPesDCcjlNlZNU0bYAUNaPMcviVJmaXLxtp0Wjqw10owK4qBl9cii92dTHPZl_VO9cZOBY_vh9dqeaca-8"
            },
            {
                "id": 3,
                "name": "Bayer Aspirin",
                "generic_name": "Aspirin",
                "dosage": "325mg",
                "form": "Tablet",
                "category": "Pain Relief",
                "price": 8.50,
                "description": "Heart health and general pain relief.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAHh65MlrOy0gXZ5krgoLInlkUBWl7rZe7cOPQyKzNOZU5idwjzju_KaI-ZGWRvYzbT4-6l5GuxPcezkmBWSt2f1XYoyk6E1XMXnPVRzj3LtLjaAcC17oSw23bwCd7KuTzakjSBZeFl0VhXXaovKoslkyIDflqDNEesoAaGNzn4NGRkSOKGrkWWFp2uo85Ohp44R03X2vLhAADUyzZGPq8xGqN3Jt3fIMR01dQgA4Laf87lkwSz4TG9rM9PKaCPsuQ5GXxcP65o3u0"
            },
            {
                "id": 4,
                "name": "MS Contin",
                "generic_name": "Morphine",
                "dosage": "15mg",
                "form": "Extended Release Tablet",
                "category": "Opioid Analgesic",
                "prescription_required": True,
                "price": 150.00,
                "description": "Severe pain management.",
                "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCIiK_UHc364SxjKyLV3cXn7KWmqFjHybdBAtUnfkNgppEozpLTIRw3hnpzxLKQdnSUN3ajBmsTtbgWwPwaKu0Xpa6EZWdW-OaMa_pAAZlfMSp3xq3DDCy6a0E9travDJCvavL2dp-B877k2Biqd3dccgfjBdYQ4ktz5OdzutTFeL2KejayAn_lyERvWDoOzhASuIpgUk5LrFmKr68qpptIg2TI-R4ZQa4yK1elMZKyx0DztLLqFNhpXZpv-VlA0qaGka4hn8dRavE"
            }
        ]

        for p_data in products:
            p = Product(**p_data)
            db.session.add(p)

        db.session.commit()
        print("Catalog seed data loaded successfully.")

if __name__ == "__main__":
    load_catalog_seed()
