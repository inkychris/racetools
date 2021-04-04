class UnrecognisedPacketType(ValueError):
    """
    Raised when numerical packet type
    does not correspond to a packet structure.
    """
    def __init__(self, value):
        super().__init__(f'unrecognised packet type value {value}')


class PacketSizeMismatch(ValueError):
    """
    Raised when trying to create a packet structure
    from data that is not the correct size.
    """
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        super().__init__(f'expected packet data size of {self.expected}, got {self.actual}')
