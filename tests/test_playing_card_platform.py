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

            assert CardSuit.query.get("C").name == "Clubs"
            assert CardSuit.query.get("S").name == "Spades"
            assert CardValue.query.get("A").name == "Ace"
            assert CardValue.query.get("A").high_value == 14
            assert CardValue.query.get("A").low_value == 1
            assert CardValue.query.get("K").name == "King"
            assert AreaType.query.get(1).name == "DECK"
            assert AreaType.query.get(4).name == "TRASH"

            self.suits = CardSuit.query.order_by("id").all()
            self.values = CardValue.query.order_by("low_value").all()
            self.area_types = AreaType.query.order_by("id").all()

            assert len(self.suits) == 4
            assert len(self.values) == 13
            assert len(self.area_types) == 4

        with self.subTest("Create New Deck"):
            self.deck = methods.new_deck()
            assert len(Deck.query.all()) == 1
            assert len(Card.query.all()) == 52

            cards = defaultdict(set)
            for card in Card.query.filter_by(deck=self.deck):
                cards[card.suit_id].add(card.value_id)
            for suit in self.suits:
                assert set([value.id for value in self.values]) == cards[suit.id]

            self.deck_2 = methods.new_deck()
            assert len(Deck.query.all()) == 2

            for deck in Deck.query:
                assert len(Card.query.filter_by(deck=deck).all()) == 52

        with self.subTest("Create New Area"):
            self.deck_area = methods.new_area("Deck Area", "DECK")
            assert self.deck_area.name == "Deck Area"

            self.play_area = methods.new_area("Play Area", "PLAY_AREA")
            assert len(Area.query.all()) == 2

            self.play_area_type = AreaType.query.filter_by(name="PLAY_AREA").one()
            assert len(self.play_area_type.areas) == 1
            assert self.play_area_type.areas[0].name == "Play Area"

            self.hand_area = methods.new_area("Hand Area", "HAND")
            assert len(Area.query.all()) == 3

        with self.subTest("Deal Cards"):
            card_1 = methods.deal_card(self.deck.id, self.play_area.id)
            assert card_1.suit_id == "C"
            assert card_1.value_id == "A"
            assert card_1.dealt
            assert card_1.area == self.play_area
            assert card_1.area_position == 0
            assert card_1.deck_position is None
            assert not card_1.face_up

            deck_cards = Card.query.filter_by(deck=self.deck, dealt=False).order_by("deck_position").all()
            assert len(deck_cards) == 51
            for i, card in enumerate(deck_cards):
                assert card.deck_position == i
                assert not card.face_up

            card_2 = methods.deal_card(self.deck.id, self.play_area.id, face_up=True)
            assert card_2.suit_id == "C"
            assert card_2.value_id == "2"
            assert card_2.dealt
            assert card_2.area == self.play_area
            assert card_2.area_position == 1
            assert card_2.deck_position is None
            assert card_2.face_up

            deck_cards = Card.query.filter_by(deck=self.deck, dealt=False).order_by("deck_position").all()
            assert len(deck_cards) == 50
            for i, card in enumerate(deck_cards):
                assert card.deck_position == i
                assert not card.face_up

        with self.subTest("Move Cards"):
            cards = Card.query.filter_by(area=self.play_area).order_by("area_position").all()
            assert cards[0].value_id == "A"
            assert cards[1].value_id == "2"

            card = methods.move_card(cards[1].id, self.play_area.id, self.hand_area.id)
            assert card == cards[1]
            assert cards[1].area == self.hand_area
            assert cards[1].area_position == 0
            assert not cards[1].face_up
            assert cards[0].area == self.play_area
            assert cards[0].area_position == 0
            assert not cards[0].face_up

            card = methods.move_card(cards[0].id, self.play_area.id, self.hand_area.id, True)
            assert card == cards[0]
            assert cards[1].area == self.hand_area
            assert cards[1].area_position == 0
            assert not cards[1].face_up
            assert cards[0].area == self.hand_area
            assert cards[0].area_position == 1
            assert cards[0].face_up

            card = methods.move_card(cards[1].id, self.hand_area.id, self.play_area.id, True)
            assert card == cards[1]
            assert cards[1].area == self.play_area
            assert cards[1].area_position == 0
            assert cards[1].face_up
            assert cards[0].area == self.hand_area
            assert cards[0].area_position == 0
            assert cards[0].face_up

        with self.subTest("Flip Card"):
            card = Card.query.filter_by(area=self.play_area).one()
            assert card.face_up

            flipped_card = methods.flip_card(card.id)
            assert flipped_card == card
            assert not card.face_up

            flipped_card = methods.flip_card(card.id)
            assert flipped_card == card
            assert card.face_up

        with self.subTest("Recall Deck"):
            deck = methods.recall_deck(self.deck.id)
            assert deck == self.deck

            shuffled = False
            deck_cards = Card.query.filter_by(deck=self.deck).order_by("deck_position").all()
            assert len(deck_cards) == 52
            for i, card in enumerate(deck_cards):
                assert not card.dealt
                assert card.deck_position == i
                assert card.area_position is None
                assert card.area_id is None
                assert not card.face_up
                if card.id - 1 != i:
                    shuffled = True
            assert shuffled

        with self.subTest("Sort Deck"):
            deck = methods.sort_deck(self.deck.id)
            assert deck == self.deck

            shuffled = False
            deck_cards = Card.query.filter_by(deck=self.deck).order_by("deck_position").all()
            assert len(deck_cards) == 52
            for i, card in enumerate(deck_cards):
                assert not card.dealt
                assert card.deck_position == i
                assert card.area_position is None
                assert card.area_id is None
                assert not card.face_up
                if card.id - 1 != i:
                    shuffled = True
            assert not shuffled

        with self.subTest("Shuffle Deck"):
            deck = methods.shuffle_deck(self.deck.id)
            assert deck == self.deck

            shuffled = False
            deck_cards = Card.query.filter_by(deck=self.deck).order_by("deck_position").all()
            assert len(deck_cards) == 52
            for i, card in enumerate(deck_cards):
                assert not card.dealt
                assert card.deck_position == i
                assert card.area_position is None
                assert card.area_id is None
                assert not card.face_up
                if card.id - 1 != i:
                    shuffled = True
            assert shuffled
