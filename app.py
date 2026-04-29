from flask import Flask, render_template, jsonify
import os
from catalog.models.product import db
from catalog.routes.catalog_api import catalog_api

app = Flask(
    __name__,
    static_folder="frontend/static",
    template_folder="frontend/pages"
)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(catalog_api)

with app.app_context():
    db.create_all()
    from seed import seed_data
    seed_data()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/product/<int:product_id>")
def product_page(product_id):
    return render_template("product.html", product_id=product_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
