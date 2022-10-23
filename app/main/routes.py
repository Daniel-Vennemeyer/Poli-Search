from flask import current_app, flash, json, make_response, redirect, url_for, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("main/index.html")


@bp.route("/information", methods=["POST"])
def information():
    print(request.form['user-input'])
    form = CookiesForm()
    return render_template("information.html", title="Information", form=form)


@bp.route("/survey", methods=["GET", "POST"])
def survey():
    form = CookiesForm()
    return render_template("survey.html", title="Survey", form=form)

@bp.route("/about_us", methods=["GET", "POST"])
def about_us():
    form = CookiesForm()
    return render_template("about_us.html", title="About Us", form=form)


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html", title="Privacy notice")


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    current_app.logger.error("{}: {} - {}".format(error.code, error.name, request.url))
    return render_template("error.html", title=error.name, error=error), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    current_app.logger.error("{}: {} - {}".format(error.code, error.description, request.url))
    flash("The form you were submitting has expired. Please try again.", "info")
    return redirect(request.full_path)
