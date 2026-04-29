from flask import Blueprint, request, jsonify, render_template
from app.auth.services import auth_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    user, error = auth_service.register_user(email, password, name)

    if error:
        return jsonify({
            "status": "error",
            "data": None,
            "error": error
        }), 400

    return jsonify({
        "status": "success",
        "data": {
            "user": user.to_dict()
        },
        "error": None
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    user, error = auth_service.login_user(email, password)

    if error:
        return jsonify({
            "status": "error",
            "data": None,
            "error": error
        }), 401

    return jsonify({
        "status": "success",
        "data": {
            "user": user.to_dict()
        },
        "error": None
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_service.logout_user()
    return jsonify({
        "status": "success",
        "data": None,
        "error": None
    })

@auth_bp.route('/me', methods=['GET'])
def me():
    user = auth_service.get_current_user()
    if not user:
        return jsonify({
            "status": "error",
            "data": None,
            "error": "Unauthorized"
        }), 401

    return jsonify({
        "status": "success",
        "data": {
            "user": user.to_dict()
        },
        "error": None
    })
