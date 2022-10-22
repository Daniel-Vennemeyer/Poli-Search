import requests
from requests.auth import HTTPBasicAuth

def get_elections_online_data():
    try:
        url = "https://www.googleapis.com/civicinfo/v2/elections"
        headers = {'X-goog-api-key': 'AIzaSyCJvZXYJQQlgH2YzinPMUpbD22NbKiD36k'}
        req = requests.get(url, headers=headers)

        return req.json()["elections"]
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error


data = get_elections_online_data()