import requests
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

def get_representatives():
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

data = get_elections()
data = get_representatives()