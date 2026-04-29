from ... import db

class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False) # Maps to Catalog Product ID
    stock = db.Column(db.Integer, default=0)

    store = db.relationship('Store')
