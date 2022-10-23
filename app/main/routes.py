from flask import current_app, flash, json, make_response, redirect, url_for, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm
from app.main import data_retrieval

global user_input

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("main/index.html")


@bp.route("/information", methods=["POST"])
def information():
    user_input = request.form['user-input']
    #officials_list = data_retrieval.get_officials()
    #official = data_retrieval.search_officials(user_input, officials_list)
    #party = data_retrieval.get_party(official)
    info = data_retrieval.get_wiki_info(user_input)
    print(user_input)
    #print(officials_list)
    #print(official)
    #print(party)
    print(info)
    return render_template("information.html", title="Information", user_input=user_input, info=info)


@bp.route("/survey", methods=["GET", "POST"])
def survey():
    return render_template("survey.html", title="Survey")

@bp.route("/about_us", methods=["GET", "POST"])
def about_us():
    return render_template("about_us.html", title="About Us")


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
