__version__ = "0.1.0"

from flask import Flask
from flask_cors import CORS

from .models import db, migrate
from .routes import socketio


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    socketio.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    return app


from . import routes  # noqa: E402, F401
from . import models  # noqa: E402, F401
from . import methods  # noqa: E402, F401


# from random import shuffle


# SUITS = ["C", "D", "H", "S"]
# VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]


# class Card:
#     """Represents a single Playing Card"""

#     def __init__(self, suit, value, deck, owner):
#         self.suit = suit
#         self.value = value
#         self.faceUp = False
#         self.deck = deck
#         self.owner = owner

#     def reveal(self):
#         self.faceUp = True

#     def peek(self):
#         return {"suit": self.suit, "value": self.value}

#     def move(self, new_owner):
#         self.owner.release(self)
#         self.owner = new_owner


# class Deck:
#     """Represents a Deck of cards"""

#     def __init__(self):
#         pass
#         # self.all_cards = [Card(suit, value, self, self) for suit in SUITS for value in VALUES]
#         # self.cards = [card for card in self.all_cards]

#     def shuffle(self):
#         shuffle(self.cards)

#     def collect(self):
#         for card in self.cards:
#             card.move(self)
#         self.cards = [card for card in self.cards]

#     def release(self, card):


# class Hand:
#     """Represents a Player's Hand of Cards"""

#     def __init__(self, args):
#         pass


# class Player:
#     """Represents a Player"""

#     def __init__(self, args):
#         pass


# class Game:
#     """Represents a Game"""

#     def __init__(self, args):
#         pass


# class Table:
#     """Represents the play Table"""

#     def __init__(self, args):
#         pass


# class CommunityCards:
#     """Represents the cards shared by the players during the game"""

#     def __init__(self, args):
#         pass


# class CommunityDiscards:
#     """Represents the community discards pile"""

#     def __init__(self, args):
#         pass
