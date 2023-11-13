import hashlib
import string
def SHA_2(arg):
	return hashlib.sha256(hashlib.sha256(arg).digest()).digest()
	#double SHA256 used to sign the message to avoid a birthday conflict

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count+=1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def encode_base58_checksum(b):
    return encode_base58(b + SHA_2(b)[:4])

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


###EXercise 7
def little_endian_to_int(i):
    """
    Takes Python bytes, interprets as little-endian
    and returns the number (assumes hex)
    in Little-Endian, THe LSB is stored first
    """
    return int.from_bytes(i, 'little')

def int_to_little_endian(integer, byte_len):
    """
    Takes Python integers, and 
    returns little-endian bytes of lenght
    byte_len
    """
    return integer.to_bytes(byte_len, 'little')
def read_varint(s):
    """
    This function reads varints
    """
    i = s.read(1)[0]
    #case 1
    if i == 0xfd:
        ##0xfd means the next 2 bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        ##0xfe means that the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        #0xff means that the next 8 bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        ##no encoding done on the original number
        return i

def encode_varint(i):
    """The function encodes integers to varints"""

    """Number less than 253"""
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        """
        Number btwn 253 and (2^16) - 1
        """
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        """
        Number btwn 2^16 and (2^32)-1
        """
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        """
        Number btwn (2^32) and (2^64) - 1
        """
        return b'\xff' + int_to_little_endian(i, 8)

