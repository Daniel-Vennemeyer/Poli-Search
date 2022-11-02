import requests
import wikipediaapi
import flask


def get_sim_value(survey_result="Survey result - N/A"):
    return survey_result


class official():
    def __init__(self, name):
        self.name = name
        self.openfec_key = 'szr3iTkQTg9eZYOhFwvWKB49mFlACXOzqMV7uJut'
        self.id = self.get_candidate_id()
        self.committee_id = self.get_committee_id()
        self.history = self.get_history(self.id)
        self.party = self.get_party()

    def get_wiki_info(self):
        try:
            wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
            page = wiki.page(self.name)
            self.name = page.title

            summary = page.summary

            heading = ""
            for section in page.sections:
                if 'Political positions' in section.title:
                    heading = page.sections[page.sections.index(section) + 1].title
            positions = page.text.split("Political positions")[1].split(heading)[0]

            return (summary, positions)
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return (error, 'POLITICIAN NOT FOUND')

    def get_name(self):
        return self.name

    def get_image_name(self):
        if self.party.lower() == 'republican party':
            image = flask.url_for('static', filename='republican.png')
        else:
            image = flask.url_for('static', filename='democratic.png')
        return image

    def get_candidate_id(self):
        try:
            url = f'https://api.open.fec.gov/v1/names/candidates/?api_key={self.openfec_key}&q={self.name.replace(" ", "%20")}'
            req = requests.get(url)
            return req.json()["results"][0]['id']
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error

    def get_committees(self, id):
        try:
            url = f"https://api.open.fec.gov/v1/candidate/{id}/committees/?page=1&per_page=20&sort_null_only=false&api_key={self.openfec_key}&sort_nulls_last=false&sort_hide_null=false&sort=name"
            req = requests.get(url)
            return req.json()['results'][0]['name']
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error

    def get_filings(self, id):
        try:
            url = f"https://api.open.fec.gov/v1/candidate/{id}/filings/?page=1&sort_nulls_last=false&sort=-receipt_date&per_page=20&sort_null_only=false&api_key={self.openfec_key}&sort_hide_null=false"
            req = requests.get(url)
            return req.json()['results'][0]
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error

    def get_committee_id(self):
        try:
            url = f"https://api.open.fec.gov/v1/names/committees/?api_key={self.openfec_key}&q={self.name.replace(' ', '%20')}"
            req = requests.get(url)
            return req.json()['results'][0]['id']
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error

    def get_history(self, id):
        try:
            url = f"https://api.open.fec.gov/v1/candidate/{id}/?page=1&sort_nulls_last=false&sort=name&per_page=20&sort_null_only=false&api_key={self.openfec_key}&sort_hide_null=false"
            req = requests.get(url)
            return req.json()['results'][0]
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error

    def get_party(self):
        return self.history['party_full'] if 'party_full' in self.history else "PARTY NOT FOUND"

    def get_finances(self):
        try:
            committee_id = official.get_committee_id(official.get_candidate_id(self.name))
            url = f"https://api.open.fec.gov/v1/committee/{committee_id}/totals/?api_key={self.openfec_key}&sort_nulls_last=false&page=1&sort_hide_null=false&per_page=20&sort=-cycle&sort_null_only=false"
            req = requests.get(url)
            finances = req.json()['results'][0]
            fin_str = ""
            for item in finances:
                fin_str += f"{item}: {finances[item]}\n"
            return fin_str
        except Exception as e:
            error = f"{type(e).__name__} exception: {e.args!r}"
            return error


# official = official("Bernie Sanders")
# info = official.get_wiki_info()
# id = official.get_candidate_id("Bernie Sanders")
# info = official.get_committee_id(id)
# info = official.get_history(id)
# info = official.get_party_v2(id)
# finances = official.get_finances("Robert Portman")
