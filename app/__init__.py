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

    # Create tables + seed a demo course on first run
    with app.app_context():
        db.create_all()

        from .models import Course

        if Course.query.count() == 0:
            demo = Course(code="CMPE 131-01", title="Demo Course")
            db.session.add(demo)
            db.session.commit()

    return app