from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
    FloatField,
)
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    role = SelectField(
        "Role",
        choices=[("student", "Student"), ("instructor", "Instructor")],
        default="student",
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Account")


class AssignmentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    due_date = DateField("Due Date", validators=[Optional()])
    submit = SubmitField("Save Assignment")


class GradeForm(FlaskForm):
    total_score = FloatField(
        "Total Score",
        validators=[Optional(), NumberRange(min=0)],
    )
    general_comment = TextAreaField("General Comment", validators=[Optional()])
    submit = SubmitField("Save Grade")