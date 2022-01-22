import requests

# No rate limits?
class TMDB:
    def get_key(self):
        # TODO - pull from db
        return ""

    def get_person_releases(self, person: str):
        key = self.get_key()
        result = requests.get(
            f"https://api.themoviedb.org/3/person/{person}/combined_credits?api_key={key}"
        )
        return self.parse_releases(result.text)

    def get_series_releases(self, series: str):
        raise Exception("TODO")

    def parse_releases(self, xml: dict):
        return xml
