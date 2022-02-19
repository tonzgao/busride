from ..base import db

# TODO: consider making this a materialized view (then query on user or releases date of result)
async def get_recent_releases(user_id: str):
    query = db.text(
        "SELECT r.entity_id AS entity_id, user_id, title, release_date, r.data AS release, i.data AS interest FROM releases r INNER JOIN interests i ON i.entity_id = r.entity_id WHERE user_id = :user_id ORDER BY release_date"
        # "SELECT r.entity_id AS entity_id, user_id, release_date, r.data AS release, i.data AS interest FROM releases r INNER JOIN interests i ON i.entity_id = r.entity_id WHERE user_id = :user_id AND release_date > NOW() - INTERVAL '1 week' AND release_date <= NOW() ORDER BY release_date"
    )
    result = await db.all(query, user_id=user_id)
    return [loader(row) for row in result]


def filter_on_interests(row, interest):
    return row  # TODO


def loader(row):
    # TODO: implement as gino loader
    return filter_on_interests(
        {
            "entity_id": row[0],
            "user_id": row[1],
            "title": row[2],
            "release_date": row[3],
            "data": row[4],
        },
        row[5],
    )
