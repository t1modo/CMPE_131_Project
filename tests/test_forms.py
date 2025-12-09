from app.forms import LoginForm, RegistrationForm


def test_login_form_requires_valid_email(app):
    form = LoginForm(data={"email": "not-an-email", "password": "pass123"})
    assert not form.validate()
    assert "Invalid email address." in form.email.errors[0]


def test_registration_passwords_must_match(app):
    form = RegistrationForm(
        data={
            "email": "new@example.com",
            "password": "password123",
            "confirm_password": "different",
            "role": "student",
        }
    )
    assert not form.validate()
    assert any("must match" in err for err in form.confirm_password.errors)