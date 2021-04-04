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


class TestStructFromTypeValue(unittest.TestCase):
    def assertStructMapping(self, value, expected_struct):
        self.assertEqual(expected_struct, pcars_udp.packet_structure(value))

    def test_telemetry_data(self):
        self.assertStructMapping(0, pcars_udp.TelemetryData)

    def test_race_data(self):
        self.assertStructMapping(1, pcars_udp.RaceData)

    def test_participants_data(self):
        self.assertStructMapping(2, pcars_udp.ParticipantsData)

    def test_timings_data(self):
        self.assertStructMapping(3, pcars_udp.TimingsData)

    def test_game_state_data(self):
        self.assertStructMapping(4, pcars_udp.GameStateData)

    def test_time_stats_data(self):
        self.assertStructMapping(7, pcars_udp.TimeStatsData)

    def test_participant_vehicle_names_data(self):
        self.assertStructMapping(8, pcars_udp.ParticipantVehicleNamesData)

    def test_invalid_value(self):
        with self.assertRaises(pcars_udp.UnrecognisedPacketType) as ex:
            pcars_udp.packet_structure(9)
        self.assertIn('9', str(ex.exception))
