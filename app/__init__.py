from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(test_config=None):
    # Setup template and static folders for the integrated frontend
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder='frontend/templates',
                static_folder='frontend/static')

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'app.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        # Core Intelligence Module
        from .core.routes.core_api import core_bp
        app.register_blueprint(core_bp)

        # User & Authentication Module
        from .auth.routes.auth_api import auth_bp
        app.register_blueprint(auth_bp)

        # Delivery & Inventory (OPS) Module
        from .ops.routes.ops_api import ops_bp
        app.register_blueprint(ops_bp)

        # Product & Catalog Module
        from .catalog.routes.catalog_api import catalog_bp
        app.register_blueprint(catalog_bp)

        # Frontend Module
        from .frontend.routes import frontend_bp
        app.register_blueprint(frontend_bp)

        # Create database tables
        from .core.models import substance, interaction, symptom, mapping, mechanism
        from .auth.models.user import User
        from .ops.models import store, inventory, reservation
        from .catalog.models.product import Product

        db.create_all()

    return app
