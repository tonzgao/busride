import arrow
from sqlalchemy import and_

from app.models.orm.entity import Entity
from app.models.orm.release import Release

from ..libs.logger import logger

from .parsers.igdb import IGDB
from .parsers.musicbrainz import MusicBrainz
from .parsers.openlibrary import OpenLibrary
from .parsers.tmdb import TMDBPerson, TMDBSeries


class EntityChecker:
    def __init__(self) -> None:
        self.parsers = {
            "P4985": TMDBPerson(),  # TV Person
            "P4983": TMDBSeries(),  # TV Series
            # "P9650": IGDB(),  # Video Game Company or Publisher
            # TODO: Video Game Series
            "P434": MusicBrainz(),  # Artist
            "P648": OpenLibrary(),  # Author
            # TODO: Book Series
        }

    async def check_entity(self, entity):
        now = arrow.utcnow()
        for key, data in self.parse_entity(entity):
            releases = await self.parse_releases(key, data)
            await self.generate_new_releases(releases, entity)
        # Touch entity to prevent rerunning on next check_releases call
        await entity.update(updated_on=now.naive).apply()

    def parse_entity(self, entity: Entity):
        claims = entity.data["claims"]
        for key, value in claims.items():
            if key in self.parsers:
                yield key, value[0]

    async def parse_releases(self, key: str, data: dict) -> "list[Release]":
        parser = self.parsers[key]
        try:
            return await parser.get_releases(data)
        except Exception as e:
            logger.warn(f"Error parsing {key}")
            raise e

    async def generate_new_releases(
        self, releases: "list[Release]", entity: Entity
    ) -> Release:
        for release in releases:
            release_date = release["release_date"]
            if (entity.updated_on != entity.created_on) and (
                release_date < entity.updated_on
            ):
                continue
            logger.info(
                f"{entity.identifier} {release['title']} {release['release_date']}"
            )
            await self.create_or_update_release(release, entity)

    async def create_or_update_release(
        self, release: Release, entity: Entity
    ) -> Release:
        current = await Release.query.where(
            and_(
                Release.title == release["title"],
                Release.entity_id == entity.id,
            )
        ).gino.first()
        release["release_date"] = release["release_date"].naive
        if current:
            return await current.update(**release, entity_id=entity.id).apply()
        return await Release.create(**release, entity_id=entity.id)


entity_checker = EntityChecker()


async def check_entity(ctx, entity):
    # TODO: should pull entity from entity id instead
    # TODO: dedupe based on entity.updated_on - confirming entity.created_on isn't the same
    await entity_checker.check_entity(entity)
