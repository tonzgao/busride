from ..base import db

# TODO: consider making this a materialized view (then query on user or releases date of result)
async def get_recent_releases(user_id: str):
    query = db.text(
        "SELECT r.entity_id AS entity_id, user_id, release_date, r.data AS release, i.data AS interest FROM releases r INNER JOIN interests i ON i.entity_id = r.entity_id WHERE user_id = :user_id AND release_date > NOW() - INTERVAL '1 week' AND release_date < NOW()"
    )
    return await db.all(query, user_id=user_id)
