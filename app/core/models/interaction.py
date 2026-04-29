from .. import db

class Interaction(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    substance_a_id = db.Column(db.Integer, db.ForeignKey('substances.id'), nullable=False)
    substance_b_id = db.Column(db.Integer, db.ForeignKey('substances.id'), nullable=False)
    severity = db.Column(db.String(50)) # e.g., 'critical', 'moderate', 'low'
    risk_score = db.Column(db.Float)
    mechanism = db.Column(db.Text)
    description = db.Column(db.Text)
    confidence = db.Column(db.Float, default=0.0)
    source = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)

    substance_a = db.relationship('Substance', foreign_keys=[substance_a_id])
    substance_b = db.relationship('Substance', foreign_keys=[substance_b_id])
