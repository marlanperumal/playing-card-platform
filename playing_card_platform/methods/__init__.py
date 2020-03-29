from random import shuffle

from .. import db
from ..models import Deck, Card, CardSuit, CardValue, Area, AreaType

SUITS = {"C": "Clubs", "D": "Diamonds", "H": "Hearts", "S": "Spades"}

VALUES = {
    "A": "Ace",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eighty",
    "9": "Nine",
    "T": "Ten",
    "J": "Jack",
    "Q": "Queen",
    "K": "King",
}

AREA_TYPES = {1: "DECK", 2: "HAND", 3: "PLAY_AREA", 4: "TRASH"}


def populate_metadata():
    CardSuit.query.delete()
    CardValue.query.delete()
    AreaType.query.delete()

    for id, name in SUITS.items():
        suit = CardSuit()
        suit.id = id
        suit.name = name
        db.session.add(suit)

    i = 1
    for id, name in VALUES.items():
        value = CardValue()
        value.id = id
        value.name = name
        value.low_value = i
        value.high_value = len(VALUES) + 1 if i == 1 else i
        db.session.add(value)
        i += 1

    for id, name in AREA_TYPES.items():
        area_type = AreaType()
        area_type.id = id
        area_type.name = name
        db.session.add(area_type)

    db.session.commit()


def new_deck():
    deck = Deck()
    deck.active = True
    deck.background = "blue"
    db.session.add(deck)
    i = 0
    for suit in CardSuit.query.all():
        for value in CardValue.query.all():
            name = f"{value.name} of {suit.name}"
            card = Card()
            card.deck = deck
            card.suit = suit
            card.value = value
            card.name = name
            card.deck_position = i
            i += 1
            db.session.add(card)
    db.session.commit()
    return deck


def new_area(name, area_type_name):
    area = Area()
    area.name = name
    area_type = AreaType.query.filter_by(name=area_type_name).one()
    area.area_type = area_type
    db.session.add(area)
    db.session.commit()
    return area


def shuffle_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck, dealt=False).all()
    shuffle(cards)
    for i, card in enumerate(cards):
        card.deck_position = i
    db.session.commit()
    return deck


def sort_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck, dealt=False).order_by("id").all()
    for i, card in enumerate(cards):
        card.deck_position = i
    db.session.commit()
    return deck


def deal_card(deck_id, area_id, face_up=False):
    cards = Card.query.filter_by(deck_id=deck_id, dealt=False).order_by("deck_position").all()
    area = Area.query.get(area_id)
    card = cards[0]
    card.dealt = True
    card.area_position = len(area.cards)
    card.area_id = area_id
    card.face_up = face_up
    card.deck_position = None
    for deck_card in cards[1:]:
        deck_card.deck_position -= 1
    db.session.commit()
    return card


def move_card(card_id, from_area_id, to_area_id, face_up=False):
    card = Card.query.get(card_id)
    to_area = Area.query.get(to_area_id)
    card.face_up = face_up
    card.area_position = len(to_area.cards)
    card.area_id = to_area_id
    from_cards = Card.query.filter_by(area_id=from_area_id).order_by("area_position")
    for i, from_card in enumerate(from_cards):
        from_card.area_position = i
    db.session.commit()
    return card


def flip_card(card_id):
    card = Card.query.get(card_id)
    card.face_up = not card.face_up
    db.session.commit()
    return card


def recall_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck).all()
    shuffle(cards)
    for i, card in enumerate(cards):
        card.dealt = False
        card.area = None
        card.deck_position = i
        card.area_position = None
        card.face_up = False
    db.session.commit()
    return deck
