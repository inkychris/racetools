class UnrecognisedPacketType(ValueError):
    """
    Raised when numerical packet type
    does not correspond to a packet structure.
    """
    def __init__(self, value, version):
        super().__init__(f'unrecognised packet type value={value}, version={version}')


class PacketSizeMismatch(ValueError):
    """
    Raised when trying to create a packet structure
    from data that is not the correct size.
    """
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        super().__init__(f'expected packet data size of {self.expected}, got {self.actual}')


class StreamWriteError(ValueError):
    """
    Raised when the number of bytes written to a stream
    does not match the number expected.
    """
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        super().__init__(f'expected to write {self.expected} bytes to stream, wrote {self.actual}')


class MissingPacket(ValueError):
    """
    Raised when attempting to retrieve data
    from a packet that hasn't been received yet.
    """
    def __init__(self, packet_type):
        self.packet_type = packet_type
        super().__init__(f'packet of type {packet_type.__qualname__} could not be found')
