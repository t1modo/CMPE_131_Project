from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User of the system (student or instructor)."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="student")  # "student" or "instructor"

    # Relationships
    enrollments = db.relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")
    submissions = db.relationship("Submission", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Course(db.Model):
    """Course, e.g., CMPE 131."""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False)   # e.g., "CMPE 131-01"
    title = db.Column(db.String(255), nullable=True)

    # Relationships
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.code}>"


class Enrollment(db.Model):
    """Bridge table: which users belong to which courses (and as what role)."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="student")

    user = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")


class Assignment(db.Model):
    """Assignment within a course."""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", back_populates="assignments")
    submissions = db.relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
    rubric_items = db.relationship("RubricItem", back_populates="assignment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assignment {self.title} ({self.course.code})>"


class Submission(db.Model):
    """Student submission for an assignment."""
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Float, nullable=True)
    general_comment = db.Column(db.Text, nullable=True)
    # For now, just store a path to the uploaded PDF (page-splitting can be added later)
    file_path = db.Column(db.String(512), nullable=True)

    assignment = db.relationship("Assignment", back_populates="submissions")
    student = db.relationship("User", back_populates="submissions")
    rubric_scores = db.relationship("SubmissionRubricScore", back_populates="submission", cascade="all, delete-orphan")


class RubricItem(db.Model):
    """Single rubric line item for an assignment (e.g., 'Correct algorithm')."""
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_points = db.Column(db.Float, nullable=False, default=1.0)

    assignment = db.relationship("Assignment", back_populates="rubric_items")
    scores = db.relationship("SubmissionRubricScore", back_populates="rubric_item", cascade="all, delete-orphan")


class SubmissionRubricScore(db.Model):
    """Score for a rubric item on a specific submission."""
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submission.id"), nullable=False)
    rubric_item_id = db.Column(db.Integer, db.ForeignKey("rubric_item.id"), nullable=False)
    points = db.Column(db.Float, nullable=True)
    comment = db.Column(db.Text, nullable=True)

    submission = db.relationship("Submission", back_populates="rubric_scores")
    rubric_item = db.relationship("RubricItem", back_populates="scores")