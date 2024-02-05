import re

def invert_bytes(content):
    byte_array = bytearray(content)
    for i in range(len(byte_array)):
        byte_array[i] = ~byte_array[i] & 0xFF
    inverted_content = bytes(byte_array)
    return inverted_content
