from .base import Base, db

# TODO: create graphql graphene query for user -> interests -> entities -> releases


class Interest(Base):
    __tablename__ = "interests"
    user_id = db.Column(
        db.BigInteger, db.ForeignKey("users.id"), nullable=False
    )
    entity_id = db.Column(
        db.BigInteger, db.ForeignKey("entities.id"), nullable=False
    )
    data = db.Column(db.JSONB)
