from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # We validated successfully; real auth not required for prototype
        flash("Not implemented", "warning")
        # Redirect so refresh doesn't resubmit the POST
        return redirect(url_for("auth.login"))
    # If GET or validation errors, render template (errors will show)
    return render_template("auth/login.html", form=form, next=request.args.get("next"))
