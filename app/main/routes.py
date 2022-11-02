from glob import glob
from flask import current_app, flash, json, make_response, redirect, session, url_for, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main import data_retrieval

global user_input


@bp.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     session["user_input"] = request.form['user-input']
    return render_template("main/index.html")


# @bp.route("/information", methods=["GET", "POST"])
@bp.route("/information", methods=["POST"])
def information():
    # # user_input = "Joe Biden"
    #
    # official = data_retrieval.official(user_input)
    # party = official.party
    # image = official.get_image_name()
    # info = official.get_wiki_info()
    # finances = official.get_finances()
    # return render_template("information.html", title="Information", user_input=user_input, info=info,
    #                        party=party, official=official, image=image, finances=finances, result="")

    if request.method == "POST":
        user_input = request.form['user-input']
        # user_input = request.form.get('user-input')
        # user_input = session["user_input"]
        # user_input = "Joe Biden"

        official = data_retrieval.official(user_input)
        party = official.party
        image = official.get_image_name()
        info = official.get_wiki_info()
        finances = official.get_finances()
        return render_template("information.html", title="Information", user_input=user_input, info=info,
                               party=party, official=official, image=image, finances=finances, result=result)
    else:
        return render_template("information.html", title="", user_input="", info="",
                           party="", official="", image="", finances="", result="")


@bp.route("/survey", methods=["GET", "POST"])
def survey():
    # demo_count, repub_count = 0, 0
    if request.method == "POST":
        dem_count = 0
        dem_count += 1 if request.form.get('pol-stance') == "Democratic" else 0
        dem_count += 1 if request.form.get('abortion') == "Pro-choice" else 0
        dem_count += 1 if request.form.get('fiscally') == "Fiscally-liberal" else 0
        dem_count += 1 if request.form.get('gun_law') == "Yes" else 0
        dem_count += 1 if request.form.get('LGBTQ') == "Yes" else 0
        # pol_stance = request.form.get('pol-stance')
        # if pol_stance == "Democratic":
        #     demo_count += 1
        # else:
        #     repub_count += 1

        # abortion = request.form.get('abortion')
        # if abortion == "Pro-choice":
        #     demo_count += 1
        # else:
        #     repub_count += 1

        # fiscally = request.form.get('fiscally')
        # if fiscally == "Fiscally-liberal":
        #     demo_count += 1
        # else:
        #     repub_count += 1

        # gun_law = request.form.get('gun_law')
        # if gun_law == "Yes":
        #     demo_count += 1
        # else:
        #     repub_count += 1

        # lgbtq = request.form.get('LGBTQ')
        # if lgbtq == "Yes":
        #     demo_count += 1
        # else:
        #     repub_count += 1

        # if demo_count > repub_count:
        #     result = (f"You are {(demo_count * 100 // 5)}% Democratic")
        # else:
        #     result = (f"You are {(repub_count * 100 // 5)}% Republican")

        if dem_count > 3:
            result = (f"You are {(dem_count * 100 // 5)}% Democratic")
        else:
            result = (f"You are {(100 - (dem_count * 100 // 5))}% Republican")

        session['result'] = result

    return render_template("survey.html", title="Survey")


# @bp.route("/about_us", methods=["GET", "POST"])
@bp.route("/about_us", methods=["GET"])
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
