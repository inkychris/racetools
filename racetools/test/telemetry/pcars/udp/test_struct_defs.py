import ctypes
import unittest

import racetools.telemetry.pcars.udp as pcars_udp


class TestStructSizes(unittest.TestCase):
    def assertStructSize(self, struct):
        self.assertEqual(struct.SIZE, ctypes.sizeof(struct))

    def test_packet_base(self):
        self.assertStructSize(pcars_udp.PacketBase)

    def test_telemetry_data(self):
        self.assertStructSize(pcars_udp.TelemetryData)

    def test_race_data(self):
        self.assertStructSize(pcars_udp.RaceData)

    def test_participants_data(self):
        self.assertStructSize(pcars_udp.ParticipantsData)

    def test_timings_data(self):
        self.assertStructSize(pcars_udp.TimingsData)

    def test_game_state_data(self):
        self.assertStructSize(pcars_udp.GameStateData)

    def test_time_stats_data(self):
        self.assertStructSize(pcars_udp.TimeStatsData)

    def test_participant_vehicle_names_data(self):
        self.assertStructSize(pcars_udp.ParticipantVehicleNamesData)

    def test_vehicle_class_names_data(self):
        self.assertStructSize(pcars_udp.VehicleClassNamesData)
