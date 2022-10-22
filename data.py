import requests
from requests.auth import HTTPBasicAuth

def get_elections_online_data():
    # api_url = "https://www.electionsonline.com/rest/v2/elections"
    # api_url ="https://www.googleapis.com/civicinfo/v2/elections"
    # response = requests.get(api_url)
    # return response.json()
    try:
        url = "https://www.googleapis.com/civicinfo/v2/elections"
        headers = {'Accept': 'application/json'}
        auth = HTTPBasicAuth('apikey', 'AIzaSyCGhhuR17suf5OmZRGF7DOFoNmGE6eQaME')
        # files = {'file': open('filename', 'rb')}
        req = requests.get(url, headers=headers, auth=auth)


        # requests.get(url, auth=(username, 1234567890123456789012345678901234567890))


        return req.json()
    except Exception as e:
        error = f"{type(e).__name__} exception: {e.args!r}"
        return error


data = get_elections_online_data()
data = get_elections_online_data()