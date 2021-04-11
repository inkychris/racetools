import queue
import socket
import threading
import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class Socket(pcars_udp.Socket):
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    def close(self) -> None:
        self._socket.close()

    def send(self, packet: bytes) -> None:
        self._socket.sendto(packet, ('127.0.0.1', pcars_udp.PORT))


class TestSocket(unittest.TestCase):
    def setUp(self) -> None:
        self._terminate_thread = threading.Event()
        self._socket = Socket()
        self.packets = queue.Queue()
        self._thread = threading.Thread(target=self._send_packet)
        self._thread.start()

    def tearDown(self) -> None:
        self._terminate_thread.set()
        self._thread.join()
        self._socket.close()

    def _send_packet(self):
        while not self._terminate_thread.is_set():
            try:
                packet = self.packets.get(timeout=0.01)
                if packet:
                    self._socket.send(packet)
                self.packets.task_done()
            except queue.Empty:
                continue

    def test_valid_packets(self):
        with pcars_udp.Socket() as udp_socket:
            self.packets.put(pcars_udp.TelemetryData(
                base=pcars_udp.PacketBase(
                    packet_type=pcars_udp.TelemetryData.TYPE,
                    packet_version=pcars_udp.TelemetryData.VERSION,
                    partial_packet_index=1,
                    partial_packet_number=1),
                speed=123.45))
            self.packets.put(pcars_udp.GameStateData(
                base=pcars_udp.PacketBase(
                    packet_type=pcars_udp.GameStateData.TYPE,
                    packet_version=pcars_udp.GameStateData.VERSION,
                    partial_packet_index=1,
                    partial_packet_number=1),
                track_temperature=25))
            self.assertAlmostEqual(123.45, udp_socket.receive().speed, places=3)
            self.assertEqual(25, udp_socket.receive().track_temperature)

    def test_invalid_packet(self):
        with pcars_udp.Socket() as udp_socket:
            self.packets.put(bytes(500))
            with self.assertRaises(racetools.errors.UnrecognisedPacketType):
                udp_socket.receive()

    def test_timeout(self):
        with pcars_udp.Socket(timeout=0.01) as udp_socket:
            with self.assertRaises(racetools.errors.Timeout):
                udp_socket.receive()
