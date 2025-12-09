import pytest
from app import create_app
from app.models import db, User, Course
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,  # make WTForms easy to test
        LOGIN_DISABLED=False,
    )

    with app.app_context():
        db.create_all()

        # Seed a sample course so the dashboard has something to show
        course = Course(code="CMPE 131-01", title="Software Engineering")
        db.session.add(course)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def instructor_user(app):
    """Create an instructor account for route / login tests."""
    from app.models import User

    u = User(
        email="instructor@example.com",
        password_hash=generate_password_hash("password123"),
        role="instructor",
    )
    db.session.add(u)
    db.session.commit()
    return u