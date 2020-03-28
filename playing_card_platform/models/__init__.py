from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


class CardSuit(db.Model):
    __table_name__ = "card_suit"
    id = db.Column(db.String(1), primary_key=True)
    name = db.Column(db.String(10))


class CardValue(db.Model):
    __table_name__ = "card_value"
    id = db.Column(db.String(1), primary_key=True)
    name = db.Column(db.String(10))
    low_value = db.Column(db.Integer)
    high_value = db.Column(db.Integer)


class Card(db.Model):
    __table_name__ = "card"
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id", ondelete="CASCADE"))
    suit_id = db.Column(db.String(1), db.ForeignKey("card_suit.id", ondelete="CASCADE"))
    value_id = db.Column(db.String(1), db.ForeignKey("card_value.id", ondelete="CASCADE"))
    name = db.Column(db.String(20))
    dealt = db.Column(db.Boolean, default=False)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id", ondelete="SET NULL"))
    deck_position = db.Column(db.Integer)
    area_position = db.Column(db.Integer)
    face_up = db.Column(db.Boolean, default=False)

    deck = db.relationship("Deck", backref="cards")
    suit = db.relationship("CardSuit", backref="cards")
    value = db.relationship("CardValue", backref="cards")
    area = db.relationship("Area", backref="cards")


class Deck(db.Model):
    __table_name__ = "deck"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    background = db.Column(db.String(20))


class AreaType(db.Model):
    __table_name__ = "area_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(255))


class Area(db.Model):
    __table_name__ = "area"
    id = db.Column(db.Integer, primary_key=True)
    area_type_id = db.Column(db.Integer, db.ForeignKey("area_type.id", ondelete="CASCADE"))
    name = db.Column(db.String(50))

    area_type = db.relationship("AreaType", backref="areas")
