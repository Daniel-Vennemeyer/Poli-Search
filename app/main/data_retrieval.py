import requests
from difflib import SequenceMatcher
import wikipedia
import flask

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_elections():
    try:
        url = "https://www.googleapis.com/civicinfo/v2/elections"
        headers = {'X-goog-api-key': 'AIzaSyCJvZXYJQQlgH2YzinPMUpbD22NbKiD36k'}
        req = requests.get(url, headers=headers)

        return req.json()["elections"]
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_officials():
    try:
        url = "https://www.googleapis.com/civicinfo/v2/representatives"
        headers = {'X-goog-api-key': 'AIzaSyCJvZXYJQQlgH2YzinPMUpbD22NbKiD36k'}
        #addresses = ['45040','Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois', 'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana', 'Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Oklahoma','Oregon','Pennsylvania', 'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
        addresses = ['45040']
        officials = []
        for address in addresses:
            query = {'address': address}
            req = requests.get(url, headers=headers, params=query)
            if "officials" in req.json():
                for official in req.json()["officials"]:
                    if official not in officials:
                        officials.append(official)
        return officials
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def search_officials(name, officials):
    try:
        sim_list = []
        for official in officials:
            sim_list.append((official['name'],similar(official['name'], name)))
            if similar("joe biden", name) > .8:
                name = "joseph r biden"
            if similar(official['name'], name) > .7:
                return official
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_official_photo(official):
    return official['photoUrl'] if 'photoUrl' in official else "NO PHOTO"

def get_party(official):
    return official['party'] if 'party' in official else "NO PARTY"

def get_wiki_info(name):
    try:
        # if official:
            # urls = official['urls'] if 'urls' in official else ""
            # if urls:
            #     for url in urls:
            #         wiki_url = url if "wikipedia" in url else ""
            # if wiki_url:
            #     response = requests.get(url=wiki_url)
            #     title = BeautifulSoup(response.content, 'html.parser').find(id="firstHeading").string

        title = wikipedia.search(name, results=1)[0]
        if title.lower() == "joe biden":
            title = "joe bide"

        summary = wikipedia.summary(title)
        content = wikipedia.page(title).content.split("==")

        heading = ""
        for section in content:
            if 'Political positions' in section:
                heading = section
        if heading:
            positions = content[content.index(heading)+1] if content[content.index(heading)+1] else content[content.index(heading)+2]
        else:
            positions = ""

        return (summary, positions)
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return 'POLITICIAN NOT FOUND'

def get_image_name(party):
    if party == 'Republican Party':
        image = flask.url_for('static', filename='republican.png')
    else:
        image = flask.url_for('static', filename='democratic.png')
    return image

def get_candidate_id(name):
    try:
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        fname,lname=name.split(" ")
        url = f"https://api.open.fec.gov/v1/names/candidates/?api_key={key}&q={fname}%20{lname}"
        req = requests.get(url)
        return req.json()["results"][0]['id']
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_committees(id):
    try:
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        url = f"https://api.open.fec.gov/v1/candidate/{id}/committees/?page=1&per_page=20&sort_null_only=false&api_key={key}&sort_nulls_last=false&sort_hide_null=false&sort=name"
        req = requests.get(url)
        return req.json()['results'][0]['name']
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_filings(id):
    try:
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        url = f"https://api.open.fec.gov/v1/candidate/{id}/filings/?page=1&sort_nulls_last=false&sort=-receipt_date&per_page=20&sort_null_only=false&api_key={key}&sort_hide_null=false"
        req = requests.get(url)
        return req.json()['results'][0]
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_committee_id(id):
    try:
        name = get_committees(id)
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        url = f"https://api.open.fec.gov/v1/names/committees/?api_key={key}&q={name.replace(' ', '%20')}"
        req = requests.get(url)
        return req.json()['results'][0]['id']
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_history(id):
    try:
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        url = f"https://api.open.fec.gov/v1/candidate/{id}/?page=1&sort_nulls_last=false&sort=name&per_page=20&sort_null_only=false&api_key={key}&sort_hide_null=false"
        req = requests.get(url)
        return req.json()['results'][0]
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def get_finances(name):
    try:
        committee_id = get_committee_id(get_candidate_id("Robert Portman"))
        key= "szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut"
        url = f"https://api.open.fec.gov/v1/committee/{committee_id}/totals/?api_key={key}&sort_nulls_last=false&page=1&sort_hide_null=false&per_page=20&sort=-cycle&sort_null_only=false"
        req = requests.get(url)
        finances = req.json()['results'][0]
        fin_str = ""
        for item in finances:
            fin_str += f"{item}: {finances[item]}\n"
        return fin_str
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error


id = get_candidate_id("Robert Portman")
info = get_committee_id(id)
# finances = get_finances(info)
finances = get_finances("Robert Portman")
