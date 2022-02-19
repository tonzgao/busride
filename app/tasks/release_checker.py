import arrow
from app.models.orm.entity import Entity
from app.models.orm.release import Release
from arq import cron
from sqlalchemy import and_

from .parsers.musicbrainz import MusicBrainz
from .parsers.openlibrary import OpenLibrary
from .parsers.tmdb import TMDB
from .parsers.igdb import IGDB


class ReleaseChecker:
    def __init__(self, now: arrow.Arrow = arrow.utcnow()) -> None:
        self.last_run = now.shift(days=-1)  # TODO: set last run in redis
        self.parsers = {
            "P4985": TMDB(),
            "P9650": IGDB(),
            "P434": MusicBrainz(),
            "P648": OpenLibrary(),
        }

    async def check_releases(self):
        entities = await self.get_entities()
        for entity in entities:
            for key, data in self.parse_entity(entity):
                releases = self.parse_releases(key, data)
                await self.generate_new_releases(releases, entity)

    async def get_entities(self):
        entities = (
            await Entity.query.where(
                True
                # Entity.updated_on < self.last_run.naive
            )
            .order_by(Entity.updated_on)
            .gino.all()
        )
        return entities

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


async def run_release_checker(ctx):
    release_checker = ReleaseChecker()
    await release_checker.check_releases()


releases_cron = cron(run_release_checker, hour=1, run_at_startup=True)
