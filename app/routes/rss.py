import arrow
import pprint
from fastapi import APIRouter
from feedgen.feed import FeedGenerator

from app.models.orm.queries.recent_releases import get_recent_releases

router = APIRouter()


def generate_feed(releases):
    fg = FeedGenerator()
    fg.title("Busride Feed")
    fg.description("Are we there yet?")
    fg.link(href="busride")

    for release in releases:
        print(release)
        fe = fg.add_entry()
        fe.id(release["title"])
        fe.title(release["title"])
        fe.pubDate(arrow.get(release["release_date"]).format())
        fe.description(pprint.pformat(release["data"]))

    rssfeed = fg.rss_str(pretty=True)
    return rssfeed


# TODO: use hashed "secure" url instead of just id
# TODO: cache result
@router.get("/rss/{user_id}/feed")
async def get_rss(user_id: int):
    releases = await get_recent_releases(user_id)
    return generate_feed(releases)
