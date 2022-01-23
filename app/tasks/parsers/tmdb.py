import requests

from app.models.orm.api import Api
from app.models.pydantic.api import ApiEnum

# No rate limits?
class TMDB:
    async def get_key(self):
        return await Api.get_key(ApiEnum.tmdb)

    async def get_person_releases(self, person: str):
        key = await self.get_key()
        result = requests.get(
            f"https://api.themoviedb.org/3/person/{person}/combined_credits?api_key={key}"
        )
        return self.parse_releases(result.text)

    def get_series_releases(self, series: str):
        raise Exception("TODO")

    def parse_releases(self, xml: dict):
        return xml
