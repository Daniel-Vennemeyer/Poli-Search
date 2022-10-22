import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from difflib import SequenceMatcher

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
        query = {'address': '3038 Taylor Ave Cincinnati OH'}
        req = requests.get(url, headers=headers, params=query)

        return req.json()["officials"]
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

def search_officials(name):
    try:
        officials = get_officials()
        sim_list = []
        for official in officials:
            sim_list.append((official['name'],similar(official['name'], name)))
            if similar(official['name'], name) > .5:
                return official
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

# def get_official_photo(name):
#     official = search_officials(name)
#     return official['photoUrl'] if 'photoUrl' in official else "NO PHOTO"

def get_official_photo(official):
    return official['photoUrl'] if 'photoUrl' in official else "NO PHOTO"

def get_party(official):
    return official['party'] if 'party' in official else "NO PARTY"

def get_wiki_info(official):
    try:
        title = ''
        urls = official['urls'] if 'urls' in official else ""
        if urls:
            for url in urls:
                wiki_url = url if "wikipedia" in url else ""
        if wiki_url:
            response = requests.get(url=wiki_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # soup = BeautifulSoup(response.content, 'lxml')
            title = soup.find(id="firstHeading")


        return title.string
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error

data = get_elections()
data = get_officials()
official = search_officials("joe biden")
official = search_officials("Rob Portman")
wiki_info = get_wiki_info(official)
photo = get_official_photo(official)
