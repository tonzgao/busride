from app.models.pydantic.entity import Entity
from app.models.orm.release import Release

from parsers.musicbrainz import MusicBrainz
from parsers.openlibrary import OpenLibrary
from parsers.tmdb import TMDB
from parsers.igdb import IGDB


class ReleaseChecker:
    def __init__(self) -> None:
        self.parsers = {
            "P4985": TMDB(),
            "P9650": IGDB(),
            "P434": MusicBrainz(),
            "P648": OpenLibrary(),
        }

    def check_releases(self):
        pass

    def get_entities(self):
        Entity.where()

    def parse_entity(self, entity: Entity):
        claims = entity["claims"]
        for key, value in claims.items():
            if key in self.parsers:
                yield key, value[0]

    def parse_releases(self, key: str, value):
        return self.parsers[key].get_releases(value)

    def generate_new_releases(self, releases: list, entity: str) -> Release:
        # TODO
        pass
