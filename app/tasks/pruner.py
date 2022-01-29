from datetime import datetime
import arrow
from arq import cron
from app.models.orm.base import db
from app.models.orm.release import Release


class Pruner:
    def __init__(self, now: datetime):
        self.cutoff = arrow.get(now).shift(weeks=-1).naive

    async def prune(self):
        await self.prune_entities()
        await self.prune_releases()

    async def prune_entities(self):
        query = db.text(
            "DELETE FROM entities e WHERE NOT EXISTS (SELECT 1 FROM interests i WHERE i.entity_id = e.id)"
        )
        await db.status(query)

    async def prune_releases(self):
        result = await Release.delete.where(
            Release.release_date < self.cutoff
        ).gino.status()
        print(result)


async def run_pruner(ctx):
    pruner = Pruner(ctx["enqueue_time"])
    await pruner.prune()


pruner_cron = cron(run_pruner, hour=0, run_at_startup=True)
