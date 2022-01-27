from .base import Base, db


class Release(Base):
    __tablename__ = "releases"
    # Title?
    entity_id = db.Column(
        db.BigInteger, db.ForeignKey("entities.id"), nullable=False
    )
    release_date = db.Column(db.DateTime, index=True)
    data = db.Column(db.JSONB)
