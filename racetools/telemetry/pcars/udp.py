import ctypes
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
        ('packet_number', ctypes.c_uint),
        ('category_packet_number', ctypes.c_uint),
        ('partial_packet_index', ctypes.c_ubyte),
        ('partial_packet_number', ctypes.c_ubyte),
        ('packet_type', ctypes.c_ubyte),
        ('packet_version', ctypes.c_ubyte),
    ]

    def struct_type(self):
        """
        Return the specialised ``Packet`` class
        based on the content of the packet base.
        Raises an ``UnrecognisedPacketType`` exception
        if the struct type cannot be determined.
        """
        if self.packet_type == 0:
            return TelemetryData
        elif self.packet_type == 1:
            return RaceData
        elif self.packet_type == 2:
            return ParticipantsData
        elif self.packet_type == 3:
            return TimingsData
        elif self.packet_type == 4:
            return GameStateData
        elif self.packet_type == 7:
            return TimeStatsData
        elif self.packet_type == 8:
            if self.partial_packet_index < self.partial_packet_number:
                return ParticipantVehicleNamesData
            elif self.partial_packet_index == self.partial_packet_number:
                return VehicleClassNamesData
        raise racetools.errors.UnrecognisedPacketType(self.packet_type)


class Packet(ctypes.Structure):
    SIZE = None


class UnpackedPacket(Packet):
    SIZE = 12
    _fields_ = [('base', PacketBase)]


class PackedPacket(Packet):
    SIZE = 12
    _pack_ = 1
    _fields_ = [('base', PacketBase)]


class TelemetryData(PackedPacket):
    SIZE = 559

    _fields_ = [
        ('viewed_participant_index', ctypes.c_char),
        ('unfiltered_throttle', ctypes.c_ubyte),
        ('unfiltered_brake', ctypes.c_ubyte),
        ('unfiltered_steering', ctypes.c_char),
        ('unfiltered_clutch', ctypes.c_ubyte),
        ('car_flags', ctypes.c_ubyte),
        ('oil_temp_celsius', ctypes.c_short),
        ('oil_pressure_kpa', ctypes.c_ushort),
        ('water_temp_celsius', ctypes.c_short),
        ('water_pressure_kpa', ctypes.c_ushort),
        ('fuel_pressure_kpa', ctypes.c_ushort),
        ('fuel_capacity', ctypes.c_ubyte),
        ('brake', ctypes.c_ubyte),
        ('throttle', ctypes.c_ubyte),
        ('clutch', ctypes.c_ubyte),
        ('fuel_level', ctypes.c_float),
        ('speed', ctypes.c_float),
        ('rpm', ctypes.c_ushort),
        ('max_rpm', ctypes.c_ushort),
        ('steering', ctypes.c_char),
        ('gear_num_gears', ctypes.c_ubyte),
        ('boost_amount', ctypes.c_ubyte),
        ('crash_state', ctypes.c_ubyte),
        ('odometer_km', ctypes.c_float),
        ('orientation', ctypes.c_float * 3),
        ('local_velocity', ctypes.c_float * 3),
        ('world_velocity', ctypes.c_float * 3),
        ('angular_velocity', ctypes.c_float * 3),
        ('local_acceleration', ctypes.c_float * 3),
        ('world_acceleration', ctypes.c_float * 3),
        ('extents_centre', ctypes.c_float * 3),
        ('tyre_flags', ctypes.c_ubyte * 4),
        ('terrain', ctypes.c_ubyte * 4),
        ('tyre_y', ctypes.c_float * 4),
        ('tyre_rps', ctypes.c_float * 4),
        ('tyre_temp', ctypes.c_ubyte * 4),
        ('tyre_height_above_ground', ctypes.c_float * 4),
        ('tyre_wear', ctypes.c_ubyte * 4),
        ('brake_damage', ctypes.c_ubyte * 4),
        ('suspension_damage', ctypes.c_ubyte * 4),
        ('brake_temp_celsius', ctypes.c_short * 4),
        ('tyre_tread_temp', ctypes.c_ushort * 4),
        ('tyre_layer_temp', ctypes.c_ushort * 4),
        ('tyre_carcass_temp', ctypes.c_ushort * 4),
        ('tyre_rim_temp', ctypes.c_ushort * 4),
        ('tyre_internal_air_temp', ctypes.c_ushort * 4),
        ('tyre_temp_left', ctypes.c_ushort * 4),
        ('tyre_temp_center', ctypes.c_ushort * 4),
        ('tyre_temp_right', ctypes.c_ushort * 4),
        ('wheel_local_position_y', ctypes.c_float * 4),
        ('ride_height', ctypes.c_float * 4),
        ('suspension_travel', ctypes.c_float * 4),
        ('suspension_velocity', ctypes.c_float * 4),
        ('suspension_ride_height', ctypes.c_ushort * 4),
        ('air_pressure', ctypes.c_ushort * 4),
        ('engine_speed', ctypes.c_float),
        ('engine_torque', ctypes.c_float),
        ('wings', ctypes.c_ubyte * 2),
        ('hand_brake', ctypes.c_ubyte),
        ('aero_damage', ctypes.c_ubyte),
        ('engine_damage', ctypes.c_ubyte),
        ('joy_pad0', ctypes.c_uint),
        ('d_pad', ctypes.c_ubyte),
        ('tyre_compound', (ctypes.c_char * TYRE_NAME_LENGTH_MAX) * 4),
        ('turbo_boost_pressure', ctypes.c_float),
        ('full_position', ctypes.c_float * 3),
        ('brake_bias', ctypes.c_ubyte),
        ('tick_count', ctypes.c_uint)
    ]


class RaceData(UnpackedPacket):
    SIZE = 308

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
        ('laps_time_in_event', ctypes.c_ushort),
        ('enforced_pit_stop_lap', ctypes.c_char),
    ]


class ParticipantsData(UnpackedPacket):
    SIZE = 1136

    _fields_ = [
        ('participants_changed_timestamp', ctypes.c_uint),
        ('name', (ctypes.c_char * PARTICIPANT_NAME_LENGTH_MAX) * PARTICIPANTS_PER_PACKET),
        ('nationality', ctypes.c_uint * PARTICIPANTS_PER_PACKET),
        ('index', ctypes.c_ushort * PARTICIPANTS_PER_PACKET),
    ]


class ParticipantsInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('world_position', ctypes.c_short * 3),
        ('orientation', ctypes.c_short * 3),
        ('current_lap_distance', ctypes.c_ushort),
        ('race_position', ctypes.c_ubyte),
        ('sector', ctypes.c_ubyte),
        ('highest_flag', ctypes.c_ubyte),
        ('pit_mode_schedule', ctypes.c_ubyte),
        ('car_index', ctypes.c_ushort),
        ('race_state', ctypes.c_ubyte),
        ('current_lap', ctypes.c_ubyte),
        ('current_time', ctypes.c_float),
        ('current_sector_time', ctypes.c_float),
        ('participant_index', ctypes.c_ushort),

    ]


class TimingsData(PackedPacket):
    SIZE = 1063

    _fields_ = [
        ('num_participants', ctypes.c_char),
        ('participants_changed_timestamp', ctypes.c_uint),
        ('event_time_remaining', ctypes.c_float),
        ('split_time_ahead', ctypes.c_float),
        ('split_time_behind', ctypes.c_float),
        ('split_time', ctypes.c_float),
        ('participants', ParticipantsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
        ('local_participant_index', ctypes.c_ushort),
        ('tick_count', ctypes.c_uint),
    ]


class GameStateData(UnpackedPacket):
    SIZE = 24

    _fields_ = [
        ('build_version_number', ctypes.c_ushort),
        ('game_state', ctypes.c_char),
        ('ambient_temperature', ctypes.c_char),
        ('track_temperature', ctypes.c_char),
        ('rain_density', ctypes.c_ubyte),
        ('snow_density', ctypes.c_ubyte),
        ('wind_speed', ctypes.c_char),
        ('wind_direction_x', ctypes.c_char),
        ('wind_direction_y', ctypes.c_char),
    ]


class ParticipantStatsInfo(ctypes.Structure):
    _fields_ = [
        ('fastest_lap_time', ctypes.c_float),
        ('last_lap_time', ctypes.c_float),
        ('last_sector_time', ctypes.c_float),
        ('fastest_sector1_time', ctypes.c_float),
        ('fastest_sector2_time', ctypes.c_float),
        ('fastest_sector3_time', ctypes.c_float),
        ('participant_online_rep', ctypes.c_uint),
        ('participant_index', ctypes.c_ushort),
    ]


class ParticipantsStats(ctypes.Structure):
    _fields_ = [
        ('participants', ParticipantStatsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
    ]


class TimeStatsData(UnpackedPacket):
    SIZE = 1040  # SMS header off by 16

    _fields_ = [
        ('participants_changed_timestamp', ctypes.c_uint),
        ('stats', ParticipantsStats),
    ]


class VehicleInfo(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_ushort),
        ('class', ctypes.c_uint),
        ('name', ctypes.c_char * VEHICLE_NAME_LENGTH_MAX),
    ]


class ParticipantVehicleNamesData(UnpackedPacket):
    SIZE = 1164

    _fields_ = [
        ('vehicles', VehicleInfo * VEHICLES_PER_PACKET),
    ]


class ClassInfo(ctypes.Structure):
    _fields_ = [
        ('class_index', ctypes.c_uint),
        ('name', ctypes.c_char * CLASS_NAME_LENGTH_MAX),
    ]


class VehicleClassNamesData(UnpackedPacket):
    SIZE = 1452

    _fields_ = [
        ('classes', ClassInfo * CLASSES_SUPPORTED_PER_PACKET),
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
        write_count = self._stream.write(packet_size_data)
        write_count += self._stream.write(packet)
        if write_count != packet.SIZE + 2:
            raise racetools.errors.StreamWriteError(packet.SIZE + 2, write_count)
