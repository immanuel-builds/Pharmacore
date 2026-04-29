from catalog.models.product import db, Product

def seed_data():
    products = [
        {
            "name": "Crocin 500",
            "generic_name": "Paracetamol",
            "dosage": "500mg",
            "form": "Tablet",
            "category": "Pain Relief",
            "price": 20.0,
            "stock": 100,
            "prescription_required": False,
            "description": "Crocin 500 tablet helps relieve pain and fever by blocking the release of certain chemical messengers responsible for fever and pain.",
            "usage": "Take one tablet every 4-6 hours as needed.",
            "warnings": "Do not exceed recommended dose. Avoid alcohol.",
            "confidence": 0.99,
            "source": "PharmaDB"
        },
        {
            "name": "Brufen 400",
            "generic_name": "Ibuprofen",
            "dosage": "400mg",
            "form": "Tablet",
            "category": "Pain Relief",
            "price": 35.0,
            "stock": 50,
            "prescription_required": False,
            "description": "Brufen 400 tablet is a non-steroidal anti-inflammatory drug (NSAID) used to relieve pain and reduce inflammation.",
            "usage": "Take with food to avoid stomach upset.",
            "warnings": "May cause stomach bleeding. Not suitable for patients with kidney issues.",
            "confidence": 0.98,
            "source": "PharmaDB"
        },
        {
            "name": "Cetirizine 10",
            "generic_name": "Cetirizine",
            "dosage": "10mg",
            "form": "Tablet",
            "category": "Cold & Flu",
            "price": 15.0,
            "stock": 200,
            "prescription_required": False,
            "description": "Cetirizine is an antihistamine used to relieve allergy symptoms such as watery eyes, runny nose, itching eyes/nose, and sneezing.",
            "usage": "Take one tablet daily.",
            "warnings": "May cause drowsiness. Avoid driving if affected.",
            "confidence": 0.97,
            "source": "PharmaDB"
        },
        {
            "name": "Phenylephrine Combo",
            "generic_name": "Phenylephrine",
            "dosage": "10mg/500mg",
            "form": "Capsule",
            "category": "Cold & Flu",
            "price": 45.0,
            "stock": 80,
            "prescription_required": False,
            "description": "Combination medicine for relief from nasal congestion and fever associated with common cold.",
            "usage": "One capsule twice daily.",
            "warnings": "Consult a doctor if you have high blood pressure.",
            "confidence": 0.95,
            "source": "PharmaDB"
        },
        {
            "name": "Vitamin C 500",
            "generic_name": "Ascorbic Acid",
            "dosage": "500mg",
            "form": "Chewable Tablet",
            "category": "Supplements",
            "price": 10.0,
            "stock": 300,
            "prescription_required": False,
            "description": "Vitamin C supplement to boost immunity and support overall health.",
            "usage": "Chew one tablet daily.",
            "warnings": "Keep out of reach of children.",
            "confidence": 0.99,
            "source": "WellnessDB"
        },
        {
            "name": "Zinc Supplement",
            "generic_name": "Zinc Sulfate",
            "dosage": "20mg",
            "form": "Tablet",
            "category": "Supplements",
            "price": 25.0,
            "stock": 150,
            "prescription_required": False,
            "description": "Zinc supplement for immune support and wound healing.",
            "usage": "One tablet per day with food.",
            "warnings": "Long term high dose can interfere with copper absorption.",
            "confidence": 0.96,
            "source": "WellnessDB"
        },
        {
            "name": "Amoxicillin 500",
            "generic_name": "Amoxicillin",
            "dosage": "500mg",
            "form": "Capsule",
            "category": "Antibiotic",
            "price": 120.0,
            "stock": 30,
            "prescription_required": True,
            "description": "Broad-spectrum antibiotic used to treat various bacterial infections.",
            "usage": "Take full course as prescribed by the doctor.",
            "warnings": "May cause allergic reactions in some individuals.",
            "confidence": 0.99,
            "source": "PharmaDB"
        }
    ]

    for p_data in products:
        exists = Product.query.filter_by(name=p_data['name']).first()
        if not exists:
            product = Product(**p_data)
            db.session.add(product)

    db.session.commit()
    print("Database seeded successfully.")
