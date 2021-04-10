import ctypes
import unittest

import racetools.util.types as types


def c_string(content, length=16):
    array_type = ctypes.c_char * length
    result = array_type()
    result[:len(content)] = content
    return result


class TestCStringToStr(unittest.TestCase):
    def test_valid(self):
        self.assertEqual('value', types.c_string_to_str(c_string(b'value\0extra')))

    def test_unterminated(self):
        self.assertEqual('x' * 16, types.c_string_to_str(c_string(b'x' * 16)))

    def test_null_string(self):
        self.assertEqual('', types.c_string_to_str(c_string(b'\0' * 16)))
