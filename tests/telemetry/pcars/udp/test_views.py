import unittest

import racetools.telemetry.pcars.udp as pcars_udp
import racetools.telemetry.pcars.views as pcars_views


def game_state_packet(**kwargs):
    return pcars_udp.GameStateData(
        base=pcars_udp.PacketBase(
            packet_type=pcars_udp.GameStateData.TYPE,
            packet_version=pcars_udp.GameStateData.VERSION,
            partial_packet_index=1,
            partial_packet_number=1),
        **kwargs)


class TestGameView(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pcars_views.DataSet()
        self.view = pcars_views.GameView(self.data)

    def test_in_main_menu(self):
        self.data.udp.update(game_state_packet(game_state=240 + 1))
        self.assertTrue(self.view.in_main_menu)

    def test_is_playing(self):
        self.data.udp.update(game_state_packet(game_state=240 + 2))
        self.assertTrue(self.view.is_playing)

    def test_in_session_menu(self):
        self.data.udp.update(game_state_packet(game_state=240 + 4))
        self.assertTrue(self.view.in_session_menu)

    def test_session_restarting(self):
        self.data.udp.update(game_state_packet(game_state=240 + 5))
        self.assertTrue(self.view.session_restarting)

    def test_in_replay(self):
        for i in (6, 7):
            with self.subTest(game_state=i):
                self.data.udp.update(game_state_packet(game_state=240 + i))
                self.assertTrue(self.view.in_replay)

    def test_in_session(self):
        for i in range(2, 7):
            with self.subTest(game_state=i):
                self.data.udp.update(game_state_packet(game_state=240 + i))
                self.assertTrue(self.view.in_session)
