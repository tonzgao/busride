from .base import Base, db


class User(Base):
    __tablename__ = "users"
    name = db.Column(db.String(255))
    email = db.Column(db.EmailType)
