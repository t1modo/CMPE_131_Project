from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from ..models import db, Course, Assignment, Submission, RubricItem
from ..forms import AssignmentForm, GradeForm

main_bp = Blueprint("main", __name__, template_folder="../templates")


@main_bp.route("/")
def index():
    """Landing page: if logged in, go straight to dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("main/index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard view matching Sketch 2."""
    # For now, instructors see all courses; students could be filtered by enrollment.
    courses = Course.query.order_by(Course.code).all()
    selected_course_id = request.args.get("course_id", type=int)

    if courses and not selected_course_id:
        selected_course_id = courses[0].id

    selected_course = Course.query.get(selected_course_id) if selected_course_id else None

    assignments = (
        Assignment.query.filter_by(course_id=selected_course.id).order_by(Assignment.due_date)
        if selected_course
        else []
    )

    return render_template(
        "main/dashboard.html",
        courses=courses,
        selected_course=selected_course,
        assignments=assignments,
    )


@main_bp.route("/courses/<int:course_id>/assignments/new", methods=["GET", "POST"])
@login_required
def create_assignment(course_id):
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


@main_bp.route("/assignments/<int:assignment_id>/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required
def grade_submission(assignment_id, submission_id):
    """Grading view matching Sketch 3."""
    assignment = Assignment.query.get_or_404(assignment_id)
    submission = Submission.query.get_or_404(submission_id)

    form = GradeForm(obj=submission)
    rubric_items = RubricItem.query.filter_by(assignment_id=assignment.id).all()

    if form.validate_on_submit():
        submission.total_score = form.total_score.data
        submission.general_comment = form.general_comment.data
        db.session.commit()
        flash("Grade saved.", "success")
        return redirect(url_for("main.dashboard", course_id=assignment.course_id))

    # For now, original/graded pages are just placeholders; real scans can plug in here.
    return render_template(
        "main/grading.html",
        assignment=assignment,
        submission=submission,
        rubric_items=rubric_items,
        form=form,
    )