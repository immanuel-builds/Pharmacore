from ... import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    generic_name = db.Column(db.String(100)) # Link to CORE Substance name
    dosage = db.Column(db.String(50))
    form = db.Column(db.String(50)) # Tablet, Liquid, etc.
    category = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    prescription_required = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    usage = db.Column(db.Text)
    warnings = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "generic_name": self.generic_name,
            "dosage": self.dosage,
            "form": self.form,
            "category": self.category,
            "price": self.price,
            "prescription_required": self.prescription_required,
            "description": self.description,
            "usage": self.usage,
            "warnings": self.warnings,
            "image_url": self.image_url
        }
