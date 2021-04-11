from __future__ import annotations
import ctypes
import socket
import typing

import racetools.errors

PORT = 5606
MAX_PACKET_SIZE = 1500
TYRE_NAME_LENGTH_MAX = 40
PARTICIPANT_NAME_LENGTH_MAX = 64
PARTICIPANTS_PER_PACKET = 16
STREAMER_PARTICIPANTS_SUPPORTED = 32
TRACK_NAME_LENGTH_MAX = 64
VEHICLE_NAME_LENGTH_MAX = 64
CLASS_NAME_LENGTH_MAX = 20
VEHICLES_PER_PACKET = 16
CLASSES_SUPPORTED_PER_PACKET = 60


class PacketBase(ctypes.Structure):
    """
    Base class for UDP packet structures.
    """
    _fields_ = [
        ('packet_number', ctypes.c_uint32),
        ('category_packet_number', ctypes.c_uint32),
        ('partial_packet_index', ctypes.c_uint8),
        ('partial_packet_number', ctypes.c_uint8),
        ('packet_type', ctypes.c_uint8),
        ('packet_version', ctypes.c_uint8),
    ]

    def struct_type(self) -> typing.Type[Packet]:
        """
        Return the specialised ``Packet`` class
        based on the content of the packet base.
        Raises an ``UnrecognisedPacketType`` exception
        if the struct type cannot be determined.
        """
        for packet_type in (
                TelemetryData,
                RaceData,
                ParticipantsData,
                TimingsData,
                GameStateData,
                TimeStatsData):
            if self.packet_type == packet_type.TYPE and self.packet_version == packet_type.VERSION:
                return packet_type
        if self.packet_type == ParticipantVehicleNamesData.TYPE:
            if self.partial_packet_index == self.partial_packet_number:
                packet_type = VehicleClassNamesData
            else:
                packet_type = ParticipantVehicleNamesData
            if self.packet_version == packet_type.VERSION:
                return packet_type
        raise racetools.errors.UnrecognisedPacketType(self.packet_type, self.packet_version)


class Packet(ctypes.Structure):
    SIZE: int = None
    PARTIAL_ARRAY_SIZE: int = None
    TYPE: int = None
    VERSION: int = None


class UnpackedPacket(Packet):
    SIZE = 12
    _fields_ = [('base', PacketBase)]


class PackedPacket(Packet):
    SIZE = 12
    _pack_ = 1
    _fields_ = [('base', PacketBase)]


class TelemetryData(PackedPacket):
    SIZE = 559
    TYPE = 0
    VERSION = 4  # SMS header incorrect

    _fields_ = [
        ('viewed_participant_index', ctypes.c_int8),
        ('unfiltered_throttle', ctypes.c_uint8),
        ('unfiltered_brake', ctypes.c_uint8),
        ('unfiltered_steering', ctypes.c_int8),
        ('unfiltered_clutch', ctypes.c_uint8),
        ('car_flags', ctypes.c_uint8),
        ('oil_temp_celsius', ctypes.c_int16),
        ('oil_pressure_kpa', ctypes.c_uint16),
        ('water_temp_celsius', ctypes.c_int16),
        ('water_pressure_kpa', ctypes.c_uint16),
        ('fuel_pressure_kpa', ctypes.c_uint16),
        ('fuel_capacity', ctypes.c_uint8),
        ('brake', ctypes.c_uint8),
        ('throttle', ctypes.c_uint8),
        ('clutch', ctypes.c_uint8),
        ('fuel_level', ctypes.c_float),
        ('speed', ctypes.c_float),
        ('rpm', ctypes.c_uint16),
        ('max_rpm', ctypes.c_uint16),
        ('steering', ctypes.c_int8),
        ('gear_num_gears', ctypes.c_uint8),
        ('boost_amount', ctypes.c_uint8),
        ('crash_state', ctypes.c_uint8),
        ('odometer_km', ctypes.c_float),
        ('orientation', ctypes.c_float * 3),
        ('local_velocity', ctypes.c_float * 3),
        ('world_velocity', ctypes.c_float * 3),
        ('angular_velocity', ctypes.c_float * 3),
        ('local_acceleration', ctypes.c_float * 3),
        ('world_acceleration', ctypes.c_float * 3),
        ('extents_centre', ctypes.c_float * 3),
        ('tyre_flags', ctypes.c_uint8 * 4),
        ('terrain', ctypes.c_uint8 * 4),
        ('tyre_y', ctypes.c_float * 4),
        ('tyre_rps', ctypes.c_float * 4),
        ('tyre_temp', ctypes.c_uint8 * 4),
        ('tyre_height_above_ground', ctypes.c_float * 4),
        ('tyre_wear', ctypes.c_uint8 * 4),
        ('brake_damage', ctypes.c_uint8 * 4),
        ('suspension_damage', ctypes.c_uint8 * 4),
        ('brake_temp_celsius', ctypes.c_int16 * 4),
        ('tyre_tread_temp', ctypes.c_uint16 * 4),
        ('tyre_layer_temp', ctypes.c_uint16 * 4),
        ('tyre_carcass_temp', ctypes.c_uint16 * 4),
        ('tyre_rim_temp', ctypes.c_uint16 * 4),
        ('tyre_internal_air_temp', ctypes.c_uint16 * 4),
        ('tyre_temp_left', ctypes.c_uint16 * 4),
        ('tyre_temp_center', ctypes.c_uint16 * 4),
        ('tyre_temp_right', ctypes.c_uint16 * 4),
        ('wheel_local_position_y', ctypes.c_float * 4),
        ('ride_height', ctypes.c_float * 4),
        ('suspension_travel', ctypes.c_float * 4),
        ('suspension_velocity', ctypes.c_float * 4),
        ('suspension_ride_height', ctypes.c_uint16 * 4),
        ('air_pressure', ctypes.c_uint16 * 4),
        ('engine_speed', ctypes.c_float),
        ('engine_torque', ctypes.c_float),
        ('wings', ctypes.c_uint8 * 2),
        ('hand_brake', ctypes.c_uint8),
        ('aero_damage', ctypes.c_uint8),
        ('engine_damage', ctypes.c_uint8),
        ('joy_pad0', ctypes.c_uint32),
        ('d_pad', ctypes.c_uint8),
        ('tyre_compound', (ctypes.c_char * TYRE_NAME_LENGTH_MAX) * 4),
        ('turbo_boost_pressure', ctypes.c_float),
        ('full_position', ctypes.c_float * 3),
        ('brake_bias', ctypes.c_uint8),
        ('tick_count', ctypes.c_uint32)
    ]


class RaceData(UnpackedPacket):
    SIZE = 308
    TYPE = 1
    VERSION = 1

    _fields_ = [
        ('world_fastest_lap_time', ctypes.c_float),
        ('personal_fastest_lap_time', ctypes.c_float),
        ('personal_fastest_sector1_time', ctypes.c_float),
        ('personal_fastest_sector2_time', ctypes.c_float),
        ('personal_fastest_sector3_time', ctypes.c_float),
        ('world_fastest_sector1_time', ctypes.c_float),
        ('world_fastest_sector2_time', ctypes.c_float),
        ('world_fastest_sector3_time', ctypes.c_float),
        ('track_length', ctypes.c_float),
        ('track_location', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('track_variation', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('translated_track_location', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('translated_track_variation', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('laps_time_in_event', ctypes.c_uint16),
        ('enforced_pit_stop_lap', ctypes.c_int8),
    ]


class ParticipantsData(UnpackedPacket):
    SIZE = 1136
    PARTIAL_ARRAY_SIZE = PARTICIPANTS_PER_PACKET
    TYPE = 2
    VERSION = 3  # SMS header incorrect

    _fields_ = [
        ('participants_changed_timestamp', ctypes.c_uint32),
        ('name', (ctypes.c_char * PARTICIPANT_NAME_LENGTH_MAX) * PARTIAL_ARRAY_SIZE),
        ('nationality', ctypes.c_uint32 * PARTIAL_ARRAY_SIZE),
        ('index', ctypes.c_uint16 * PARTIAL_ARRAY_SIZE),
    ]


class ParticipantsInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('world_position', ctypes.c_int16 * 3),
        ('orientation', ctypes.c_int16 * 3),
        ('current_lap_distance', ctypes.c_uint16),
        ('race_position', ctypes.c_uint8),
        ('sector', ctypes.c_uint8),
        ('highest_flag', ctypes.c_uint8),
        ('pit_mode_schedule', ctypes.c_uint8),
        ('car_index', ctypes.c_uint16),
        ('race_state', ctypes.c_uint8),
        ('current_lap', ctypes.c_uint8),
        ('current_time', ctypes.c_float),
        ('current_sector_time', ctypes.c_float),
        ('participant_index', ctypes.c_uint16),

    ]


class TimingsData(PackedPacket):
    SIZE = 1063
    TYPE = 3
    VERSION = 1  # SMS header incorrect

    _fields_ = [
        ('num_participants', ctypes.c_int8),
        ('participants_changed_timestamp', ctypes.c_uint32),
        ('event_time_remaining', ctypes.c_float),
        ('split_time_ahead', ctypes.c_float),
        ('split_time_behind', ctypes.c_float),
        ('split_time', ctypes.c_float),
        ('participants', ParticipantsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
        ('local_participant_index', ctypes.c_uint16),
        ('tick_count', ctypes.c_uint32),
    ]


class GameStateData(UnpackedPacket):
    SIZE = 24
    TYPE = 4
    VERSION = 2

    _fields_ = [
        ('build_version_number', ctypes.c_uint16),
        ('game_state', ctypes.c_int8),
        ('ambient_temperature', ctypes.c_int8),
        ('track_temperature', ctypes.c_int8),
        ('rain_density', ctypes.c_uint8),
        ('snow_density', ctypes.c_uint8),
        ('wind_speed', ctypes.c_int8),
        ('wind_direction_x', ctypes.c_int8),
        ('wind_direction_y', ctypes.c_int8),
    ]


class ParticipantStatsInfo(ctypes.Structure):
    _fields_ = [
        ('fastest_lap_time', ctypes.c_float),
        ('last_lap_time', ctypes.c_float),
        ('last_sector_time', ctypes.c_float),
        ('fastest_sector1_time', ctypes.c_float),
        ('fastest_sector2_time', ctypes.c_float),
        ('fastest_sector3_time', ctypes.c_float),
        ('participant_online_rep', ctypes.c_uint32),
        ('participant_index', ctypes.c_uint16),
    ]


class ParticipantsStats(ctypes.Structure):
    _fields_ = [
        ('participants', ParticipantStatsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
    ]


class TimeStatsData(UnpackedPacket):
    SIZE = 1040  # SMS header off by 16
    TYPE = 7
    VERSION = 1  # SMS header incorrect

    _fields_ = [
        ('participants_changed_timestamp', ctypes.c_uint32),
        ('stats', ParticipantsStats),
    ]


class VehicleInfo(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_uint16),
        ('class', ctypes.c_uint32),
        ('name', ctypes.c_char * VEHICLE_NAME_LENGTH_MAX),
    ]


class ParticipantVehicleNamesData(UnpackedPacket):
    SIZE = 1164
    PARTIAL_ARRAY_SIZE = VEHICLES_PER_PACKET
    TYPE = 8
    VERSION = 2

    _fields_ = [
        ('vehicles', VehicleInfo * PARTIAL_ARRAY_SIZE),
    ]


class ClassInfo(ctypes.Structure):
    _fields_ = [
        ('class_index', ctypes.c_uint32),
        ('name', ctypes.c_char * CLASS_NAME_LENGTH_MAX),
    ]


class VehicleClassNamesData(UnpackedPacket):
    SIZE = 1452
    PARTIAL_ARRAY_SIZE = CLASSES_SUPPORTED_PER_PACKET
    TYPE = 8
    VERSION = 2

    _fields_ = [
        ('classes', ClassInfo * PARTIAL_ARRAY_SIZE),
    ]


def packet_from_bytes(data: bytes) -> Packet:
    """
    Create UDP packet structure from byte array.
    Raises a ``PacketSizeMismatch`` if the size of ``data``
    does not match the size of the struct
    determined by the packet type value pulled from ``data``.
    """
    packet = PacketBase.from_buffer_copy(data)
    struct = packet.struct_type()
    if len(data) != struct.SIZE:
        raise racetools.errors.PacketSizeMismatch(struct.SIZE, len(data))
    return struct.from_buffer_copy(data)


class PacketStream:
    """
    A wrapper around a binary IO stream
    to read/write sequential packets.
    """
    def __init__(self, stream: typing.BinaryIO):
        self._stream = stream

    def receive(self) -> [Packet, None]:
        """
        Read a header and respective packet data from the stream
        and return an instantiated ``Packet`` object.
        Returns ``None`` if no bytes are returned
        when attempting to read the packet header from the stream.
        Raises ``PacketSizeMismatch`` or ``UnrecognisedPacketType``
        if packet object instantiation fails.
        """
        packet_size_data = self._stream.read(2)
        if not packet_size_data:
            return None
        packet_size = int.from_bytes(packet_size_data, 'little')
        packet_data = self._stream.read(packet_size)
        return packet_from_bytes(packet_data)

    def send(self, packet: Packet) -> None:
        """
        Write a ``Packet`` to the stream
        including an appropriate header.
        Raises a ``StreamWriteError`` if number of bytes written
        does not match the size of the packet and header.
        """
        packet_size_data = packet.SIZE.to_bytes(2, 'little')
        write_count = self._stream.write(packet_size_data + packet)
        if write_count != packet.SIZE + 2:
            raise racetools.errors.StreamWriteError(packet.SIZE + 2, write_count)


class Socket:
    """
    Context manager to receive packets from UDP.
    """
    def __init__(self, timeout: float = None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('', PORT))
        self._socket.settimeout(timeout)

    def close(self) -> None:
        """
        Close the UDP socket.
        """
        self._socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def receive(self) -> Packet:
        """
        Read data from UDP socket
        and attempt to return a ``Packet``.
        """
        try:
            return packet_from_bytes(self._socket.recvfrom(MAX_PACKET_SIZE)[0])
        except socket.timeout:
            raise racetools.errors.PacketError('timeout reached waiting for UDP packet') from None


class Data:
    """
    Aggregate of UDP packets to be passed to views.
    """
    def __init__(self):
        self._data = {struct: {} for struct in (
            TelemetryData,
            RaceData,
            ParticipantsData,
            TimingsData,
            GameStateData,
            TimeStatsData,
            ParticipantVehicleNamesData,
            VehicleClassNamesData)}

    def update(self, packet: Packet) -> None:
        packet_type = type(packet)
        partial_index = packet.base.partial_packet_index - 1
        self._data[packet_type][partial_index] = packet

    def get(
            self,
            packet_type: typing.Type[Packet],
            key: str, *,
            array_index: int = None,
            array_key: str = None):
        partial_packet_index = 0
        if None not in (array_index, packet_type.PARTIAL_ARRAY_SIZE):
            partial_packet_index = array_index // packet_type.PARTIAL_ARRAY_SIZE
        value = self._data[packet_type].get(partial_packet_index)
        if value is None:
            raise racetools.errors.MissingPacket(packet_type)
        for component in key.split('.'):
            value = getattr(value, component)
        if array_index is not None:
            relative_index = array_index
            if packet_type.PARTIAL_ARRAY_SIZE is not None:
                relative_index %= packet_type.PARTIAL_ARRAY_SIZE
            value = value[relative_index]
        if array_key:
            value = getattr(value, array_key)
        return value
