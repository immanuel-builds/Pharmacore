import re
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.auth.models.user import User

def register_user(email, password, name):
    # Validation
    if not email or not password or not name:
        return None, "All fields are required"

    if len(password) < 6:
        return None, "Password must be at least 6 characters long"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return None, "Invalid email format"

    if User.query.filter_by(email=email).first():
        return None, "Email already exists"

    # Creation
    password_hash = generate_password_hash(password)
    new_user = User(email=email, password_hash=password_hash, name=name)

    db.session.add(new_user)
    db.session.commit()

    return new_user, None

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return None, "Invalid credentials"

    if not user.is_active:
        return None, "Account is disabled"

    session["user_id"] = user.id
    return user, None

def logout_user():
    session.pop("user_id", None)

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)
