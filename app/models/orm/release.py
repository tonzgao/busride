from .base import Base, db


class Release(Base):
    __tablename__ = "releases"
    title = db.Column(db.String(255), nullable=False)
    entity_id = db.Column(
        db.BigInteger, db.ForeignKey("entities.id"), nullable=False
    )
    release_date = db.Column(db.DateTime, index=True)
    data = db.Column(db.JSONB)
    _idx1 = db.Index(
        "release_idx_entity_title", "title", "entity_id", unique=True
    )
