from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    generic_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    form = db.Column(db.String(50))
    category = db.Column(db.String(50))

    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    prescription_required = db.Column(db.Boolean, default=False)

    description = db.Column(db.Text)
    usage = db.Column(db.Text)
    warnings = db.Column(db.Text)

    confidence = db.Column(db.Float)
    source = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "generic_name": self.generic_name,
            "dosage": self.dosage,
            "form": self.form,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "prescription_required": self.prescription_required,
            "description": self.description,
            "usage": self.usage,
            "warnings": self.warnings,
            "confidence": self.confidence,
            "source": self.source
        }
