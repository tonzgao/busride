from .base import Base, db


class Entity(Base):
    __tablename__ = "entities"
    identifier = db.Column(db.String(255), nullable=False, index=True)
    data = db.Column(db.JSONB, nullable=False)

    @classmethod
    async def get_by_identifier(cls, identifier: str):
        return await cls.query.where(cls.identifier == identifier).gino.first()
