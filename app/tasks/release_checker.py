from app.models.pydantic.entity import Entity
from app.models.orm.release import Release

from parsers.musicbrainz import MusicBrainz
from parsers.openlibrary import OpenLibrary
from parsers.tmdb import TMDB
from parsers.igdb import IGDB

parsers = {
    "P4985": TMDB(),
    "P9650": IGDB(),
    "P434": MusicBrainz(),
    "P648": OpenLibrary(),
}


def parse_entity(entity: Entity):
    claims = entity["claims"]
    for key, value in claims.items():
        if key in parsers:
            yield key, value[0]


def parse_releases(key: str, value):
    return parsers[key].get_releases(value)


def generate_new_releases(releases: list, entity: str) -> Release:
    # TODO
    pass
