from flask import url_for
from werkzeug.security import generate_password_hash
from app.models import db, User


def test_index_redirects_when_logged_in(app, client, instructor_user):
    # log in via Flask-Login manually
    login_url = "/auth/login"
    resp = client.post(
        login_url,
        data={"email": instructor_user.email, "password": "password123"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data  # title from dashboard page


def test_login_page_loads(app, client):
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data


def test_register_creates_user(app, client):
    resp = client.post(
        "/auth/register",
        data={
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "role": "student",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # flash message should contain "Account created"
    assert b"Account created" in resp.data

    user = User.query.filter_by(email="testuser@example.com").first()
    assert user is not None
    assert user.role == "student"


def test_dashboard_requires_login(app, client):
    resp = client.get("/dashboard", follow_redirects=False)
    # Flask-Login should redirect anonymous users to login page (302)
    assert resp.status_code in (302, 401)