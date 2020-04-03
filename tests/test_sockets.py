from flask import current_app

from playing_card_platform.routes import socketio
from . import BaseTest


class TestSockets(BaseTest):
    def setUp(self):
        super().setUp()
        self.socketio_client = socketio.test_client(current_app,)

    def test_connection(self):
        r = self.socketio_client.get_received()
        assert len(r) == 1
        assert r[0]["name"] == "welcome"
        assert len(r[0]["args"]) == 1
        assert r[0]["args"][0] == {"data": "test"}
