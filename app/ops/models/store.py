from ... import db

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_lng = db.Column(db.Float, nullable=False)
    radius_km = db.Column(db.Float, default=5.0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": {"lat": self.location_lat, "lng": self.location_lng},
            "radius_km": self.radius_km,
            "is_active": self.is_active
        }
