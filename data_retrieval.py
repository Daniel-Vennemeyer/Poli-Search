import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from difflib import SequenceMatcher
import wikipedia

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
        addresses = ['45040','Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois', 'Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana', 'Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Oklahoma','Oregon','Pennsylvania', 'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

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


officials_list = get_officials()
# official = search_officials("joe biden", officials_list)
info = get_wiki_info("Joe Biden")
