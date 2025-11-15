from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Minimal user model for Flask-Login."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # stub only

    def __repr__(self):
        return f"<User {self.email}>"

class Course(db.Model):
    """Simple domain model stub (e.g., used later for 'shared classes')."""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False)   # e.g., "CMPE 131"
    title = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Course {self.code}>"
