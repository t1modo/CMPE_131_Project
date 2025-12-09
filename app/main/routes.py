import os
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    send_from_directory,
    abort,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ..models import (
    db,
    Course,
    Assignment,
    Submission,
    RubricItem,
    Enrollment,
)
from ..forms import (
    AssignmentForm,
    AssignmentFileForm,
    SubmissionUploadForm,
    GradeForm,
)

main_bp = Blueprint("main", __name__, template_folder="../templates")


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("main/index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Shared entry point.
    - Instructors: see course + assignment dashboard.
    - Students: see enrolled courses + assignments and their submission status.
    """

    # INSTRUCTOR VIEW
    if current_user.role == "instructor":
        courses = Course.query.order_by(Course.code).all()
        selected_course_id = request.args.get("course_id", type=int)

        if courses and not selected_course_id:
            selected_course_id = courses[0].id

        selected_course = (
            Course.query.get(selected_course_id) if selected_course_id else None
        )

        assignments = (
            Assignment.query.filter_by(course_id=selected_course.id)
            .order_by(Assignment.due_date)
            .all()
            if selected_course
            else []
        )

        return render_template(
            "main/dashboard_instructor.html",
            courses=courses,
            selected_course=selected_course,
            assignments=assignments,
        )

    # STUDENT VIEW
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    courses = [enroll.course for enroll in enrollments]

    selected_course_id = request.args.get("course_id", type=int)
    if courses and not selected_course_id:
        selected_course_id = courses[0].id

    selected_course = (
        Course.query.get(selected_course_id) if selected_course_id else None
    )

    assignments = []
    if selected_course:
        assignments = (
            Assignment.query.filter_by(course_id=selected_course.id)
            .order_by(Assignment.due_date)
            .all()
        )

    return render_template(
        "main/dashboard_student.html",
        courses=courses,
        selected_course=selected_course,
        assignments=assignments,
    )


@main_bp.route("/courses/<int:course_id>/assignments/new", methods=["GET", "POST"])
@login_required
def create_assignment(course_id):
    if current_user.role != "instructor":
        abort(403)

    course = Course.query.get_or_404(course_id)
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            course=course,
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
        )
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment created.", "success")
        return redirect(url_for("main.dashboard", course_id=course.id))
    return render_template("main/assignment_form.html", form=form, course=course)


@main_bp.route("/assignments/<int:assignment_id>/edit", methods=["GET", "POST"])
@login_required
def edit_assignment(assignment_id):
    if current_user.role != "instructor":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    form = AssignmentForm(obj=assignment)

    if form.validate_on_submit():
        assignment.title = form.title.data
        assignment.description = form.description.data
        assignment.due_date = form.due_date.data
        db.session.commit()
        flash("Assignment updated.", "success")
        return redirect(url_for("main.dashboard", course_id=course.id))

    return render_template("main/assignment_form.html", form=form, course=course)


@main_bp.route("/assignments/<int:assignment_id>/assign-file", methods=["GET", "POST"])
@login_required
def assign_file(assignment_id):
    """
    Instructor assigns an assignment file (prompt PDF).
    This does NOT create submissions; it just stores the assignment file.
    """
    if current_user.role != "instructor":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)
    form = AssignmentFileForm()

    if form.validate_on_submit():
        file = form.assignment_file.data
        filename = secure_filename(f"assignment_{assignment.id}_{file.filename}")

        upload_folder = str(current_app.config["UPLOAD_FOLDER"])
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        assignment.prompt_file_path = filename
        db.session.commit()

        flash("Assignment file uploaded and assigned.", "success")
        return redirect(url_for("main.dashboard", course_id=assignment.course_id))

    return render_template("main/assignment_file_upload.html", assignment=assignment, form=form)


@main_bp.route("/assignments/<int:assignment_id>/submit", methods=["GET", "POST"])
@login_required
def submit_assignment(assignment_id):
    """
    Student uploads their own submission PDF.
    - If a Submission already exists for this student & assignment, update it.
    - Otherwise, create a new Submission.
    """
    if current_user.role != "student":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)

    # find existing submission for this student+assignment if any
    submission = Submission.query.filter_by(
        assignment_id=assignment.id,
        student_id=current_user.id,
    ).first()

    form = SubmissionUploadForm()
    if form.validate_on_submit():
        file = form.student_file.data
        filename = secure_filename(f"submission_{assignment.id}_{current_user.id}_{file.filename}")

        upload_folder = str(current_app.config["UPLOAD_FOLDER"])
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        if submission is None:
            submission = Submission(
                assignment=assignment,
                student=current_user,
                student_file_path=filename,
                submitted_at=datetime.utcnow(),
            )
            db.session.add(submission)
        else:
            submission.student_file_path = filename
            submission.submitted_at = datetime.utcnow()

        db.session.commit()

        flash("Submission uploaded successfully.", "success")
        return redirect(url_for("main.dashboard", course_id=assignment.course_id))

    return render_template("main/submission_upload.html", assignment=assignment, form=form, submission=submission)


@main_bp.route("/assignments/<int:assignment_id>/submissions")
@login_required
def list_submissions(assignment_id):
    """
    Instructor view: list all student submissions for an assignment.
    """
    if current_user.role != "instructor":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = (
        Submission.query.filter_by(assignment_id=assignment.id)
        .order_by(Submission.submitted_at.desc().nullslast())
        .all()
    )
    return render_template(
        "main/submissions_list.html",
        assignment=assignment,
        submissions=submissions,
    )


@main_bp.route(
    "/assignments/<int:assignment_id>/grade/<int:submission_id>",
    methods=["GET", "POST"],
)
@login_required
def grade_submission(assignment_id, submission_id):
    """
    Instructor grades a specific student's submission.
    - Can set score + comments
    - Can upload a graded PDF (returned to student)
    """
    if current_user.role != "instructor":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)
    submission = Submission.query.get_or_404(submission_id)

    if submission.assignment_id != assignment.id:
        abort(404)

    form = GradeForm(obj=submission)
    rubric_items = RubricItem.query.filter_by(assignment_id=assignment.id).all()

    if form.validate_on_submit():
        submission.total_score = form.total_score.data
        submission.general_comment = form.general_comment.data
        submission.graded_at = datetime.utcnow()

        graded_file = form.graded_file.data
        if graded_file:
            filename = secure_filename(
                f"graded_{assignment.id}_{submission.student_id}_{graded_file.filename}"
            )
            upload_folder = str(current_app.config["UPLOAD_FOLDER"])
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            graded_file.save(filepath)
            submission.graded_file_path = filename

        db.session.commit()
        flash("Grade and feedback saved.", "success")
        return redirect(
            url_for("main.list_submissions", assignment_id=assignment.id)
        )

    return render_template(
        "main/grading.html",
        assignment=assignment,
        submission=submission,
        rubric_items=rubric_items,
        form=form,
    )


@main_bp.route("/submissions/<int:submission_id>")
@login_required
def view_submission(submission_id):
    """
    Student view of their submission and feedback.
    Instructors can also open it if needed.
    """
    submission = Submission.query.get_or_404(submission_id)
    assignment = submission.assignment
    rubric_items = RubricItem.query.filter_by(assignment_id=assignment.id).all()
    return render_template(
        "main/submission_detail.html",
        submission=submission,
        assignment=assignment,
        rubric_items=rubric_items,
    )


@main_bp.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    """
    Serve uploaded PDFs (assignment prompts, student submissions, graded PDFs).
    For a real app, you'd add more security checks.
    """
    upload_folder = str(current_app.config["UPLOAD_FOLDER"])
    return send_from_directory(upload_folder, filename)