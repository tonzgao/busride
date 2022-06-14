import arrow
from arq import cron
from sqlalchemy import and_

from app.models.orm.entity import Entity
from app.models.orm.release import Release

from ..libs.logger import logger
from ..libs.redis import get_redis

from .parsers.igdb import IGDB
from .parsers.musicbrainz import MusicBrainz
from .parsers.openlibrary import OpenLibrary
from .parsers.tmdb import TMDBPerson, TMDBSeries


class ReleaseChecker:
    def __init__(self, now: arrow.Arrow = arrow.utcnow()) -> None:
        self.redis = None
        self.last_run = now.shift(days=-1)  # TODO: set last run in redis
        self.parsers = {
            "P4985": TMDBPerson(),  # TV Person
            "P4983": TMDBSeries(),  # TV Series
            "P9650": IGDB(),  # Video Game Company or Publisher
            # TODO: Video Game Series
            "P434": MusicBrainz(),  # Artist
            "P648": OpenLibrary(),  # Author
            # TODO: Book Series
        }

    async def get_last_run(self):
        self.redis = await get_redis()
        last_run = await self.redis.execute("GET", "busride-last-run")
        if last_run:
            self.last_run = arrow.get(last_run.decode("utf-8"))

    async def set_last_run(self):
        await self.redis.execute(
            "SET", "busride-last-run", str(arrow.utcnow())
        )

    async def check_releases(self):
        await self.get_last_run()
        entities = await self.get_entities()
        logger.debug(f"Checking {len(entities)} entities")
        for entity in entities:
            await self.check_entity(entity)
        await self.set_last_run()

    async def get_entities(self):
        entities = (
            await Entity.query.where(Entity.updated_on < self.last_run.naive)
            .order_by(Entity.updated_on)
            .gino.all()
        )
        return entities

    async def check_entity(self, entity):
        for key, data in self.parse_entity(entity):
            releases = await self.parse_releases(key, data)
            await self.generate_new_releases(releases, entity)

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
            if release_date < self.last_run.shift(days=-1):
                continue
            logger.info(
                f"{entity.identifier} {release['title']} {release['release_date']}"
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
