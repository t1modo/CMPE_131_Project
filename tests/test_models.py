from app.models import db, User, Course, Assignment, Submission


def test_user_role_default(app):
    u = User(email="student@example.com", password_hash="hash")
    db.session.add(u)
    db.session.commit()

    assert u.id is not None
    # default role is student
    assert u.role == "student"


def test_course_and_assignment_relationship(app):
    course = Course(code="CMPE 131-02", title="Alt Section")
    db.session.add(course)
    db.session.commit()

    assignment = Assignment(course=course, title="HW 1")
    db.session.add(assignment)
    db.session.commit()

    assert assignment.course_id == course.id
    assert assignment in course.assignments


def test_submission_links_student_and_assignment(app):
    course = Course.query.first()
    user = User(email="s1@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    assignment = Assignment(course=course, title="Midterm 1")
    db.session.add(assignment)
    db.session.commit()

    submission = Submission(assignment=assignment, student=user, file_path="dummy.pdf")
    db.session.add(submission)
    db.session.commit()

    assert submission.assignment_id == assignment.id
    assert submission.student_id == user.id
    assert submission in assignment.submissions
    assert submission in user.submissions