import io
import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class TestPacketStream(unittest.TestCase):
    def test_valid_packets(self):
        data = io.BytesIO()
        packet_stream = pcars_udp.PacketStream(data)
        packet_stream.send(pcars_udp.GameStateData(
            base=pcars_udp.PacketBase(packet_type=4),
            game_state=123,
            wind_direction_y=64))
        packet_stream.send(pcars_udp.TelemetryData(
            speed=12.34,
            brake_bias=50))
        data.seek(0)
        read_packet = packet_stream.receive()
        self.assertEqual(123, int.from_bytes(read_packet.game_state, 'little'))
        self.assertEqual(64, int.from_bytes(read_packet.wind_direction_y, 'little'))
        read_packet = packet_stream.receive()
        self.assertAlmostEqual(12.34, read_packet.speed, places=3)
        self.assertEqual(50, read_packet.brake_bias)
        self.assertIsNone(packet_stream.receive())

    def test_failed_write(self):
        class LimitedWriteBuffer(io.BytesIO):
            def __init__(self, *args, size=64, **kwargs):
                super().__init__(*args, **kwargs)
                self._size = size

            def write(self, buffer) -> int:
                written = 0
                for byte_val in bytearray(buffer):
                    written += super().write(byte_val.to_bytes(1, 'little'))
                    if self.tell() >= self._size:
                        break
                return written

        data = LimitedWriteBuffer()
        packet_stream = pcars_udp.PacketStream(data)
        with self.assertRaises(racetools.errors.StreamWriteError) as ex:
            packet_stream.send(pcars_udp.TelemetryData(
                speed=12.34))
        self.assertEqual(pcars_udp.TelemetryData.SIZE + 2, ex.exception.expected)
        self.assertEqual(64, ex.exception.actual)
