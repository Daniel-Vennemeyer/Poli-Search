import requests
from requests.auth import HTTPBasicAuth

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

            return req.json()
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error


data = get_elections()
data = get_representatives()