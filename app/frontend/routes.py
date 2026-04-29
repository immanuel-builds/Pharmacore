from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def home():
    return render_template('home.html')

@frontend_bp.route('/product/<int:product_id>')
def product(product_id):
    return render_template('product.html', product_id=product_id)
