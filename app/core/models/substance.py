from .. import db

class Substance(db.Model):
    __tablename__ = 'substances'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100))
    mechanism = db.Column(db.Text)
    half_life_hours = db.Column(db.Float)
    primary_organ = db.Column(db.String(100))
    confidence = db.Column(db.Float, default=0.0)
    source = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "mechanism": self.mechanism,
            "half_life_hours": self.half_life_hours,
            "primary_organ": self.primary_organ,
            "confidence": self.confidence,
            "source": self.source,
            "verified": self.verified
        }
