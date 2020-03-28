from collections import defaultdict

from playing_card_platform import __version__, methods
from playing_card_platform.models import db, CardSuit, CardValue, Card, Deck, AreaType, Area
from . import BaseTest


def test_version():
    assert __version__ == "0.1.0"


class TestIntegration(BaseTest):
    def test_workflow(self):
        with self.subTest("Create Metadata"):
            methods.populate_metadata()

            assert len(CardSuit.query.all()) == 4
            assert len(CardValue.query.all()) == 13
            assert len(AreaType.query.all()) == 4

            assert CardSuit.query.get("C").name == "Clubs"
            assert CardSuit.query.get("S").name == "Spades"
            assert CardValue.query.get("A").name == "Ace"
            assert CardValue.query.get("A").high_value == 14
            assert CardValue.query.get("A").low_value == 1
            assert CardValue.query.get("K").name == "King"
            assert AreaType.query.get(1).name == "DECK"
            assert AreaType.query.get(4).name == "TRASH"

        with self.subTest("Create New Deck"):
            methods.new_deck()
            assert len(Deck.query.all()) == 1
            assert len(Card.query.all()) == 52
            deck = Deck.query.first()
            cards = defaultdict(set)
            for card in Card.query.filter_by(deck=deck):
                cards[card.suit_id].add(card.value_id)
            suits = [suit.id for suit in CardSuit.query]
            values = [value.id for value in CardValue.query]
            for suit in suits:
                assert set(values) == cards[suit]
            methods.new_deck()
            assert len(Deck.query.all()) == 2
            for deck in Deck.query:
                assert len(Card.query.filter_by(deck=deck).all()) == 52

        with self.subTest("Create New Area"):
            methods.new_area("Main Deck", "DECK")
            area = Area.query.one()
            assert area.name == "Main Deck"

            methods.new_area("Play Area", "PLAY_AREA")
            assert len(Area.query.all()) == 2
            area_type = AreaType.query.filter_by(name="PLAY_AREA").one()
            assert len(area_type.areas) == 1
            assert area_type.areas[0].name == "Play Area"

            methods.new_area("Hand", "HAND")
            assert len(Area.query.all()) == 3

        with self.subTest("Deal Cards"):
            deck = Deck.query.first()
            area = Area.query.filter_by(name="Play Area").one()
            card_1 = methods.deal_card(deck.id, area.id)
            assert card_1.suit_id == "C"
            assert card_1.value_id == "A"
            assert card_1.dealt
            assert card_1.area == area
            assert card_1.area_position == 0
            assert card_1.deck_position is None
            assert not card_1.face_up

            deck_cards = Card.query.filter_by(deck=deck, dealt=False).order_by("deck_position").all()
            assert len(deck_cards) == 51
            for i, card in enumerate(deck_cards):
                assert card.deck_position == i
                assert not card.face_up

            card_2 = methods.deal_card(deck.id, area.id, face_up=True)
            assert card_2.suit_id == "C"
            assert card_2.value_id == "2"
            assert card_2.dealt
            assert card_2.area == area
            assert card_2.area_position == 1
            assert card_2.deck_position is None
            assert card_2.face_up

            deck_cards = Card.query.filter_by(deck=deck, dealt=False).order_by("deck_position").all()
            assert len(deck_cards) == 50
            for i, card in enumerate(deck_cards):
                assert card.deck_position == i
                assert not card.face_up

        with self.subTest("Move Cards"):
            area_1 = Area.query.filter_by(name="Play Area").one()
            area_2 = Area.query.filter_by(name="Hand").one()
            cards = Card.query.filter_by(area=area_1).order_by("area_position").all()
            assert cards[0].value_id == "A"
            assert cards[1].value_id == "2"

            card = methods.move_card(cards[1].id, area_1.id, area_2.id)
            assert card == cards[1]
            assert cards[1].area == area_2
            assert cards[1].area_position == 0
            assert not cards[1].face_up
            assert cards[0].area == area_1
            assert cards[0].area_position == 0
            assert not cards[0].face_up

            card = methods.move_card(cards[0].id, area_1.id, area_2.id, True)
            assert card == cards[0]
            assert cards[1].area == area_2
            assert cards[1].area_position == 0
            assert not cards[1].face_up
            assert cards[0].area == area_2
            assert cards[0].area_position == 1
            assert cards[0].face_up

            card = methods.move_card(cards[1].id, area_2.id, area_1.id, True)
            assert card == cards[1]
            assert cards[1].area == area_1
            assert cards[1].area_position == 0
            assert cards[1].face_up
            assert cards[0].area == area_2
            assert cards[0].area_position == 0
            assert cards[0].face_up

        with self.subTest("Flip Card"):
            area = Area.query.filter_by(name="Play Area").one()
            card = Card.query.filter_by(area=area).one()
            assert card.face_up

            flipped_card = methods.flip_card(card.id)
            assert flipped_card == card
            assert not card.face_up

            flipped_card = methods.flip_card(card.id)
            assert flipped_card == card
            assert card.face_up
