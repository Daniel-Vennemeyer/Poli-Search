from glob import glob
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
    officials_list = data_retrieval.get_officials()
    official = data_retrieval.search_officials(user_input, officials_list)
    party = data_retrieval.get_party(official)
    info = data_retrieval.get_wiki_info(user_input)
    image = data_retrieval.get_image_name(party)
    id = data_retrieval.get_candidate_id(user_input)
    news = data_retrieval.get_committees(id)
    print(news)
    #print(user_input)
    #print(officials_list)
    #print(official)
    #print(party)
    #print(info)
    return render_template("information.html", title="Information", user_input=user_input, info=info, 
    party=party, official=official, image=image, news=news)


@bp.route("/survey", methods=["GET", "POST"])
def survey():
    demo_count, repub_count = 0, 0
    if request.method == "POST": 
        pol_stance = request.form.get('pol-stance')
        if pol_stance == "Democratic":
            demo_count += 1

        else:
            repub_count += 1    

        abortion = request.form.get('abortion')
        if abortion == "Pro-choice":
            demo_count += 1

        else:
            repub_count += 1 

        fiscally = request.form.get('fiscally')
        if fiscally == "Fiscally-liberal":
            demo_count += 1

        else:
            repub_count += 1 

        gun_law = request.form.get('gun_law')
        if gun_law == "Yes":
            demo_count += 1

        else:
            repub_count += 1 

        lgbtq = request.form.get('LGBTQ')
        if lgbtq == "Yes":
            demo_count += 1

        else:
            repub_count += 1 

        if demo_count > repub_count:
            print(f"You are {(demo_count*100//5)}% Democratic")
        
        else:
            print(f"You are {(repub_count*100//5)}% Republican")
        
        print(lgbtq)
        stances = []
        stances.append(pol_stance)
        stances.append(globali)
        stances.append(abortion)
        stances.append(fiscally)
        stances.append(gun_law)
        stances.append(lgbtq)
    print(stances)
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
