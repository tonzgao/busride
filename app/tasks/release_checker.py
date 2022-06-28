import arrow
from arq import cron

from app.models.orm.entity import Entity

from ..libs.logger import logger
from ..libs.redis import get_redis


class ReleaseChecker:
    def __init__(self, now: arrow.Arrow = arrow.utcnow()) -> None:
        self.redis = None
        self.last_run = now.shift(days=-1)

    async def get_last_run(self):
        self.redis = await get_redis()
        last_run = await self.redis.execute("GET", "busride-last-run")
        if last_run:
            self.last_run = arrow.get(last_run)

    async def set_last_run(self):
        await self.redis.execute(
            "SET", "busride-last-run", str(arrow.utcnow())
        )

    async def check_releases(self):
        # TODO: move to job queue
        await self.get_last_run()
        entities = await self.get_entities()
        logger.debug(f"Checking {len(entities)} entities")
        for entity in entities:
            await self.push_entity(entity)
        await self.set_last_run()

    async def get_entities(self):
        entities = (
            await Entity.query.where(Entity.updated_on < self.last_run.naive)
            .order_by(Entity.updated_on)
            .gino.all()
        )
        return entities

    async def push_entity(self, entity: Entity):
        # TODO: push entity id instead of entity for when entity checker moves to separate container
        await self.redis.enqueue_job("check_entity", entity)


async def run_release_checker(ctx):
    release_checker = ReleaseChecker()
    await release_checker.check_releases()


releases_cron = cron(run_release_checker, hour=1, run_at_startup=True)
