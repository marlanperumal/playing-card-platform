from flask_testing import TestCase
from playing_card_platform import create_app, db
from config import TestConfig


class BaseTest(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app


class BaseDBTest(BaseTest):
    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.commit()
        db.session.remove()
