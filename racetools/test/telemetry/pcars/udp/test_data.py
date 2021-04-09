import unittest

import racetools.errors
import racetools.telemetry.pcars.udp as pcars_udp


class TestData(unittest.TestCase):
    def test_missing_packet(self):
        with self.assertRaises(racetools.errors.MissingPacket):
            pcars_udp.Data().get(pcars_udp.TelemetryData, 'speed')

    def test_direct_attribute(self):
        data = pcars_udp.Data()
        data.update(pcars_udp.TelemetryData(
            base=pcars_udp.PacketBase(
                partial_packet_index=1,
                partial_packet_number=1),
            speed=123.45))
        self.assertAlmostEqual(123.45, data.get(pcars_udp.TelemetryData, 'speed'), places=3)

    def test_array_attribute(self):
        data = pcars_udp.Data()

        def packet(partial_index, partial_total):
            result = pcars_udp.ParticipantsData(
                base=pcars_udp.PacketBase(
                    partial_packet_index=partial_index,
                    partial_packet_number=partial_total))
            array_size = pcars_udp.ParticipantsData.PARTIAL_ARRAY_SIZE
            for i in range(array_size):
                name = f'name_{((partial_index - 1) * array_size) + i}'
                result.name[i][:len(name)] = name.encode('utf-8')
            return result

        data.update(packet(1, 3))
        data.update(packet(2, 3))
        data.update(packet(3, 3))
        for i in (10, 20, 40):
            with self.subTest(index=i):
                self.assertEqual(f'name_{i}', data.get(pcars_udp.ParticipantsData, 'name', array_index=i))

    def test_array_sub_attribute(self):
        data = pcars_udp.Data()
        packet = pcars_udp.TimeStatsData(
            base=pcars_udp.PacketBase(
                partial_packet_index=1,
                partial_packet_number=1))
        packet.stats.participants[0].participant_online_rep = 1234
        data.update(packet)
        self.assertEqual(1234, data.get(
            pcars_udp.TimeStatsData, 'stats.participants', array_index=0, array_key='participant_online_rep'))
