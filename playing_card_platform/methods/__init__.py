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

AREA_TYPES = {"DECK": "DECK", "HAND": "HAND", "PLAY": "PLAY", "TRASH": "TRASH"}


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

    for id, description in AREA_TYPES.items():
        area_type = AreaType()
        area_type.id = id
        area_type.description = description
        db.session.add(area_type)

    db.session.commit()


def new_area(name, area_type_id):
    area = Area()
    area.name = name
    area.area_type_id = area_type_id
    db.session.add(area)
    db.session.commit()
    return area


def new_deck():
    deck = Deck()
    deck.active = True
    deck.background = "blue"
    db.session.add(deck)
    db.session.commit()
    area = new_area(f"Deck Area {deck.id}", "DECK")
    deck.area = area
    i = 0
    for suit in CardSuit.query.all():
        for value in CardValue.query.all():
            name = f"{value.name} of {suit.name}"
            card = Card()
            card.deck = deck
            card.area = deck.area
            card.suit = suit
            card.value = value
            card.name = name
            card.position = i
            i += 1
            db.session.add(card)
    db.session.commit()
    return deck


def shuffle_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck, dealt=False).all()
    shuffle(cards)
    for i, card in enumerate(cards):
        card.position = i
    db.session.commit()
    return deck


def sort_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck, dealt=False).order_by("id").all()
    for i, card in enumerate(cards):
        card.position = i
    db.session.commit()
    return deck


def order_area(area_id):
    area = Area.query.get(area_id)
    cards = Card.query.filter_by(area=area).order_by("position").all()
    for i, card in enumerate(cards):
        card.position = i
    db.session.commit()
    return area


def move_card(card_id, to_area_id, face_up=False):
    card = Card.query.get(card_id)
    from_area = card.area
    to_area = Area.query.get(to_area_id)
    card.face_up = face_up
    card.position = len(to_area.cards)
    card.area_id = to_area_id
    db.session.commit()
    order_area(from_area.id)
    db.session.commit()
    return card


def deal_card(deck_id, area_id, face_up=False):
    card = Card.query.filter_by(deck_id=deck_id, dealt=False).order_by("position").first()
    card = move_card(card.id, area_id, face_up)
    card.dealt = True
    db.session.commit()
    return card


def flip_card(card_id):
    card = Card.query.get(card_id)
    card.face_up = not card.face_up
    db.session.commit()
    return card


def recall_deck(deck_id):
    deck = Deck.query.get(deck_id)
    cards = Card.query.filter_by(deck=deck, dealt=True).all()
    affected_area_ids = set()
    for i, card in enumerate(cards):
        affected_area_ids.add(card.area_id)
        card.dealt = False
        card.area = deck.area
        card.face_up = False
    for area_id in affected_area_ids:
        order_area(area_id)
    shuffle_deck(deck_id)
    db.session.commit()
    return deck
