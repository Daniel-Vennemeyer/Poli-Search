from flask import current_app, flash, json, make_response, redirect, url_for, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.route("/index2", methods=["GET", "POST"])
def index2():
    form = CookiesForm()
    return render_template("index2.html", title="Information", form=form)


@bp.route("/index3", methods=["GET", "POST"])
def index3():
    form = CookiesForm()
    return render_template("index3.html", title="Survey", form=form)

@bp.route("/index4", methods=["GET", "POST"])
def index4():
    form = CookiesForm()
    return render_template("index4.html", title="About Us", form=form)


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
