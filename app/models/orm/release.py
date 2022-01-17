from .base import Base, db


class Release(Base):
    __tablename__ = "releases"
    entity_id = db.Column(db.BigInteger, db.ForeignKey("entities.id"), nullable=False)
    release_date = db.Column(db.DateTime)
    data = db.Column(db.JSONB)