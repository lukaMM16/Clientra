from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # import modela (da SQLAlchemy vidi tablice)
    from app.models import User, Client, Service, Appointment  # noqa: F401

    # registracija blueprinta (OBAVEZNO ovdje, ne gore)
    from app.routes.main import main_bp
    from app.routes.clients import clients_bp
    from app.routes.services import services_bp
    from app.routes.appointments import appointments_bp
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app
