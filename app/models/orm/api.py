from .base import Base, db


class Api(Base):
    __tablename__ = "apis"
    user_id = db.Column(
        db.BigInteger, db.ForeignKey("users.id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False, index=True)
    data = db.Column(db.JSONB, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    @classmethod
    async def get_key(cls, name: str):
        return (
            await cls.query.where(cls.name == name)
            .order_by(cls.updated_on)
            .gino.first()
        )
