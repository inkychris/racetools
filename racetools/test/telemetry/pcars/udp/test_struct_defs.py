import ctypes
import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class TestStructSizes(unittest.TestCase):
    def assertStructSize(self, struct):
        self.assertEqual(struct.SIZE, ctypes.sizeof(struct))

    def test_packed_packet(self):
        self.assertStructSize(pcars_udp.PackedPacket)

    def test_unpacked_packet(self):
        self.assertStructSize(pcars_udp.UnpackedPacket)

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


class TestStructType(unittest.TestCase):
    def assertStructMapping(self, packet_type, expected_struct, partial_packet_index=1, partial_packet_total=1):
        packet = pcars_udp.PacketBase.from_buffer_copy(bytearray([
            0, 0, 0, 0,
            0, 0, 0, 0,
            partial_packet_index,
            partial_packet_total,
            packet_type,
            0]))
        self.assertEqual(expected_struct, packet.struct_type())

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
        self.assertStructMapping(
            8, pcars_udp.ParticipantVehicleNamesData,
            partial_packet_index=1, partial_packet_total=2)

    def test_vehicle_class_names_data(self):
        self.assertStructMapping(
            8, pcars_udp.VehicleClassNamesData,
            partial_packet_index=2, partial_packet_total=2)

    def test_invalid_value(self):
        with self.assertRaises(racetools.errors.UnrecognisedPacketType) as ex:
            self.assertStructMapping(9, None)
        self.assertIn('9', str(ex.exception))
