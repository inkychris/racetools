def c_string_to_str(array) -> str:
    """
    Cast C-string byte array to ``str``.
    """
    return bytes(array).partition(b'\0')[0].decode('utf-8')
