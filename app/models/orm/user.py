from .base import Base, db


class User(Base):
    __tablename__ = "users"
    name = db.Column(db.String(255))
    email = db.Column(db.EmailType, nullable=False, index=True, unique=True)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.query.where(cls.email == email).gino.first()
