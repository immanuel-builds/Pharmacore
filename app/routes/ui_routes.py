from flask import Blueprint, render_template, session

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/')
def index():
    return render_template('index.html')

@ui_bp.route('/product/<int:product_id>')
def product_page(product_id):
    # Just need name for title placeholder if we wanted, but we'll fetch via JS
    return render_template('product.html', product_id=product_id)

@ui_bp.route('/login')
def login_page():
    return render_template('login.html')

@ui_bp.route('/cart')
def cart_page():
    return render_template('cart.html')
