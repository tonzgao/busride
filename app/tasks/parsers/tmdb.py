import requests
import arrow

from app.models.orm.api import Api
from app.models.pydantic.api import ApiEnum

from ...libs.logger import logger

# No rate limits?
class TMDB:
    async def get_key(self, data):
        # TODO: filter by user id
        api = await Api.get_key(ApiEnum.tmdb)
        return api.data["key"]


class TMDBPerson(TMDB):
    async def get_releases(self, data):
        person = data["mainsnak"]["datavalue"]["value"]
        key = await self.get_key(data)
        result = requests.get(
            f"https://api.themoviedb.org/3/person/{person}/combined_credits?api_key={key}"
        )
        return self.parse_releases(result.json())

    def parse_releases(self, json: dict):
        logger.debug(json)
        yield from self.parse_group(json, "cast")
        yield from self.parse_group(json, "crew")

    def parse_group(self, json, group):
        for item in json[group]:
            result = self.parse_release(item, group)
            if result:
                yield result

    def parse_release(self, release: dict, role: str):
        release_date = release.get("release_date") or release.get(
            "first_air_date"
        )
        if not release_date:
            return
        title = (
            release.get("title")
            or release.get("original_title")
            or release.get("name")
        )
        return {
            "release_date": arrow.get(release_date),
            "title": title,
            "data": {
                "type": release["media_type"],
                "role": role,  # TODO: consider attaching entity id in data (or use graph db)
            },
        }


class TMDBSeries(TMDB):
    async def get_releases(self, data):
        series = data["mainsnak"]["datavalue"]["value"]
        key = await self.get_key(data)
        result = requests.get(
            f"https://api.themoviedb.org/3/tv/{series}?api_key={key}"
        )
        return self.parse_releases(result.json())

    def parse_releases(self, json: dict):
        logger.debug(json)
        latest_release = json["last_episode_to_air"]
        if not latest_release.get("air_date"):
            return []
        return [self.parse_release(latest_release)]

    def parse_release(self, release: dict):
        return {
            "release_date": arrow.get(release["air_date"]),
            "title": release["name"],
            "data": {
                "season": release["season_number"],
                "episode": release["episode_number"],
            },
        }
