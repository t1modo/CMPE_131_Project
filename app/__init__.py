from flask import Flask
from .config import Config
from .models import db
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id: str):
    # Minimal user loader; OK if DB is empty for this prototype
    try:
        from .models import User
        return User.query.get(int(user_id))
    except Exception:
        return None

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    # Create tables on first run (safe for a prototype)
    with app.app_context():
        db.create_all()

    return app
