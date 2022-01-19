from .base import Base, db


class Entity(Base):
    __tablename__ = "entities"
    identifier = db.Column(db.String(255), nullable=False, index=True)
    data = db.Column(db.JSONB, nullable=False)
