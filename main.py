from flask import Flask, render_template, jsonify, session
import os
from app.catalog.models.product import db
from app.catalog.routes.catalog_api import catalog_api
from app.commerce.routes.commerce_api import commerce_api
from app.commerce.models.cart import CartItem
from app.commerce.models.order import Order, OrderItem

app = Flask(
    __name__,
    static_folder="frontend/static",
    template_folder="frontend/pages"
)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db.init_app(app)
app.register_blueprint(catalog_api)
app.register_blueprint(commerce_api)

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

@app.route("/shopping-cart")
def cart_page():
    return render_template("cart.html")

@app.route("/dev/login")
def dev_login():
    session["user_id"] = 1
    return "Logged in as test user 1"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
