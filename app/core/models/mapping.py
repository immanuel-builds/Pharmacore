from .. import db

class SymptomMapping(db.Model):
    __tablename__ = 'symptom_mappings'
    id = db.Column(db.Integer, primary_key=True)
    substance_id = db.Column(db.Integer, db.ForeignKey('substances.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    relevance_score = db.Column(db.Float)

    substance = db.relationship('Substance')
    symptom = db.relationship('Symptom')
