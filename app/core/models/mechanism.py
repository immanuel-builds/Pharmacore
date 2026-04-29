from .. import db

class MechanismNode(db.Model):
    __tablename__ = 'mechanism_nodes'
    id = db.Column(db.Integer, primary_key=True)
    substance_id = db.Column(db.Integer, db.ForeignKey('substances.id'), nullable=False)
    node_name = db.Column(db.String(100), nullable=False)
    node_type = db.Column(db.String(50)) # drug, enzyme, receptor, transporter
    effect = db.Column(db.String(100)) # e.g., inhibition, agonism

    substance = db.relationship('Substance')
