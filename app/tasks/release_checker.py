import arrow
from arq import cron
from sqlalchemy import and_

from app.models.orm.entity import Entity
from app.models.orm.release import Release

from ..logger import logger
from .parsers.igdb import IGDB
from .parsers.musicbrainz import MusicBrainz
from .parsers.openlibrary import OpenLibrary
from .parsers.tmdb import TMDB


class ReleaseChecker:
    def __init__(self, now: arrow.Arrow = arrow.utcnow()) -> None:
        self.last_run = now.shift(days=-1)  # TODO: set last run in redis
        self.parsers = {
            "P4985": TMDB(),  # TV Person
            "P4983": TMDB(),  # TV Series
            "P9650": IGDB(),  # Video Game Company or Publisher
            # TODO: Video Game Series
            "P434": MusicBrainz(),  # Artist
            "P648": OpenLibrary(),  # Author
            # TODO: Book Series
        }

    async def check_releases(self):
        entities = await self.get_entities()
        logger.debug(f"Checking {len(entities)} entities")
        for entity in entities:
            self.check_entity(entity)

    async def get_entities(self):
        entities = (
            await Entity.query.where(Entity.updated_on < self.last_run.naive)
            .order_by(Entity.updated_on)
            .gino.all()
        )
        return entities

    async def check_entity(self, entity):
        for key, data in self.parse_entity(entity):
            releases = self.parse_releases(key, data)
            await self.generate_new_releases(releases, entity)

    def parse_entity(self, entity: Entity):
        claims = entity.data["claims"]
        for key, value in claims.items():
            if key in self.parsers:
                yield key, value[0]

    def parse_releases(self, key: str, data: dict) -> "list[Release]":
        return self.parsers[key].get_releases(data)

    async def generate_new_releases(
        self, releases: "list[Release]", entity: Entity
    ) -> Release:
        for release in releases:
            release_date = release["release_date"]
            if release_date < self.last_run.shift(days=-1):
                continue
            logger.info(
                f"{entity.identifier} {release.title} {release.release_date}"
            )
            await self.create_or_update_release(release, entity)
        # Touch entity to prevent rerunning on next check_releases call
        entity.update(updated_on=arrow.now().datetime)

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


async def run_release_checker(ctx):
    release_checker = ReleaseChecker()
    await release_checker.check_releases()


releases_cron = cron(run_release_checker, hour=1, run_at_startup=True)
