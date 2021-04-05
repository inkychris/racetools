import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class TestPacketFromBytes(unittest.TestCase):
    def test_valid_packet(self):
        self.assertIsInstance(pcars_udp.packet_from_bytes(bytes(pcars_udp.TelemetryData.SIZE)), pcars_udp.TelemetryData)

    def test_packet_too_small(self):
        with self.assertRaises(racetools.errors.PacketSizeMismatch) as ex:
            pcars_udp.packet_from_bytes(bytes(16))
        self.assertEqual(pcars_udp.TelemetryData.SIZE, ex.exception.expected)
        self.assertIn(str(pcars_udp.TelemetryData.SIZE), str(ex.exception))
        self.assertEqual(16, ex.exception.actual)
        self.assertIn('16', str(ex.exception))

    def test_packet_too_big(self):
        with self.assertRaises(racetools.errors.PacketSizeMismatch) as ex:
            pcars_udp.packet_from_bytes(bytes(600))
        self.assertEqual(pcars_udp.TelemetryData.SIZE, ex.exception.expected)
        self.assertIn(str(pcars_udp.TelemetryData.SIZE), str(ex.exception))
        self.assertEqual(600, ex.exception.actual)
        self.assertIn('600', str(ex.exception))
