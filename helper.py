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
def lit_to_int(little, length):
    """
    Takes Python bytes, interprets as little-endian
    and returns the number (assumes hex)
    in Little-Endian, THe LSB is stored first
    """
    return little.to_bytes(length, 'little')


