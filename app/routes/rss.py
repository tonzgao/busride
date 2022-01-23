from fastapi import APIRouter
from feedgen.feed import FeedGenerator

from app.models.orm.queries.recent_releases import get_recent_releases

router = APIRouter()


def generate_feed(releases):
    fg = FeedGenerator()
    fg.title("TODO")
    fg.description("TODO")
    fg.link(href="busride")
    rssfeed = fg.rss_str(pretty=True)
    return rssfeed


# TODO: use hashed "secure" url instead of just id
# TODO: cache result
@router.get("/rss/{user_id}/feed")
async def get_rss(user_id: int):
    releases = await get_recent_releases(user_id)
    return generate_feed(releases)
