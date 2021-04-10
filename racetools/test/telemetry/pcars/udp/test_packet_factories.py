import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class TestPacketFromBytes(unittest.TestCase):
    def setUp(self) -> None:
        self.packet_base = bytes(pcars_udp.PacketBase(packet_version=4))

    def test_valid_packet(self):
        self.assertIsInstance(pcars_udp.packet_from_bytes(self.packet_base + bytes(547)), pcars_udp.TelemetryData)

    def test_packet_too_small(self):
        with self.assertRaises(racetools.errors.PacketSizeMismatch) as ex:
            pcars_udp.packet_from_bytes(self.packet_base)
        self.assertEqual(pcars_udp.TelemetryData.SIZE, ex.exception.expected)
        self.assertIn(str(pcars_udp.TelemetryData.SIZE), str(ex.exception))
        self.assertEqual(12, ex.exception.actual)
        self.assertIn('12', str(ex.exception))

    def test_packet_too_big(self):
        with self.assertRaises(racetools.errors.PacketSizeMismatch) as ex:
            pcars_udp.packet_from_bytes(self.packet_base + bytes(600))
        self.assertEqual(pcars_udp.TelemetryData.SIZE, ex.exception.expected)
        self.assertIn(str(pcars_udp.TelemetryData.SIZE), str(ex.exception))
        self.assertEqual(612, ex.exception.actual)
        self.assertIn('612', str(ex.exception))
