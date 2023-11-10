from unittest import TestCase
import hashlib
import hmac
from typing import Self
import math
from helper import hash160, encode_base58_checksum
##blockchain programming by python
"""Defining a finite field using a python class"""
class FiniteElement():
    """docstring for Finiteelement"""

    def __init__(self, element: int, prime: int): #initiate the finite field
        if type(element) == int:
            if element >= prime or element < 0: #check if element btwn 0 and prime-1
                error = 'Element {} not in the range of the finite field of 0 to {}'\
                .format(element, prime-1)
                raise ValueError(error)
        self.element= element
        self.prime = prime


    def __eq__(self, other): #equating function
        if other is None:
            return False
        return self.element == other.element and self.prime == other.prime

    def __ne__(self, other): #not equal
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            exception = 'Cannot add two elements not in the same order'
            raise TypeError(exception)
        if self == None:
            return other
        if type(self.element) == int:
            element = (self.element + other.element) % self.prime
        elif type(self.element) == FiniteElement:
            element = (self.element.element + other.element.element)  % self.prime
        return self.__class__(element, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            exception = 'Cannot subtract  two elements not in the same field'
            raise TypeError(exception)
        if type(self.element) == int:
            element = (self.element - other.element) % self.prime
        elif type(self.element) == FiniteElement:
            element = (self.element.element - other.element.element) % self.prime
        return self.__class__(element, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            exception = 'Cannot multiply elements of different fields'
            raise TypeError(exception)
        element = (self.element * other.element) % self.prime
        return self.__class__(element, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        element = pow(self.element, n, self.prime)
        return self.__class__(element % self.prime, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            exception = 'Cannot divide elements of different fields'
            raise TypeError(exception)
        element = (self.element *pow(other.element, self.prime-2, self.prime)) % self.prime
        return self.__class__(element, self.prime)
    def __repr__(self):#representation function
        return 'FieldElement_{}({})'.format(self.prime, self.element)


class Point():#defining a point on a curve using secp256k1 y^2 = x^3 + a.x^2 + b
    zero = 0
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if (self.y)**2 != (self.x)**3 + a*x + b:
            raise ValueError('Point {},{} is not on curve'.format(x, y))
        
    def __eq__(self, other):
        if other is None:
            return False
        return self.a == other.a and self.b == other.b and self.x == other.x and self.y == other.y


    def __ne__(self, other):
        return not (self == other)
        """return self.a != other.a and self.b != other.b and self.x != other.x and self.y != other.y"""


    def __add__(self, other):
        three = FiniteElement(element=3, prime=self.x.prime)
        zero = FiniteElement(element=0, prime=self.x.prime)
        if self.x == other.x and self.y == other.y and self.y == zero:
            return self.__class__(None, None, self.a, self.b)
        if self.a != other.a or self.b != other.b:
            exception = 'Points {} {} are not on the same curve'.format(self, other)
            raise TypeError(exception)

        if other.x is None:
            x = self.x
            y = self.y
        elif self.x is None:
            x = other.x
            y = other.y

        if self.x == other.x and self.y != other.y:
            x = None
            y = None

        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x = pow(slope, 2) -self.x - other.x
            y = (slope*(self.x - x)) - self.y


        if self.x == other.x and self.y == other.y:
            slope = (three*pow(self.x, 2) + self.a) / (self.y+self.y)
            x = pow(slope, 2) - (self.x+self.x)
            y = (slope*(self.x - x)) - self.y
        


        return self.__class__(x, y, self.a, self.b)
    def __rmul__(self, coefficient):    #using binary expansion
        coef = coefficient-1
        current = self
        """result0 = self.__class__(None, None, self.a, self.b)"""#start at point at infinity
        result1 = self.__class__(self.x, self.y, self.a, self.b)#due to a hiccup(slope for self ==other) up there i cannot start at 0
        while coef:
            if coef & 1: #checking the right-most bit, if 1 add 1
                result1 +=current #adding point to itself
            current += current #adding point to self again
            coef >>=1 #shifting the coeffiecient bit to the right
        return result1
    """def __rmul__(self, coefficient):
        product = self
        for _ in range(coefficient-1):
            product +=self
        return product"""


    def __repr__(self):
        if self.x == None and self.y is None:
            return 'Point ({})'.format('infinity')
        else:
            return 'Point ({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

class blockchain(TestCase):
    def test_on_curve(self):
        prime = 223
        a = FiniteElement(0, prime)
        b = FiniteElement(7, prime)

        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))


        for x_test, y_test in valid_points:
            x = FiniteElement(x_test, prime)
            y = FiniteElement(y_test, prime)
            Point(x, y, a, b)
        for x_test, y_test in invalid_points:
            x = FiniteElement(x_test, prime)
            y = FiniteElement(y_test, prime)
            Point(x, y, a, b)

        with self.assertRaises(ValueError):
            Point(x, y, a, b)           


P = (2**256) - (2**32) -977 #prime as dictated by secp256ki
A = 0 #value of a in secp256ki
B = 7 #value of b in secp256ki
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 #order of group generated by S256Point


#object below stores the signatura (r) and s
class Signature():
    def __init__(self, s, r):
        self.r = r
        self.s = s
    def __repr__(self):
        return 'Signature {:x}, {:x}'.format(self.r, self.s)

    def der(self):
        """
        Serializing a Signature
        """
        rbin = self.r.to_bytes(32, 'big')
        ##We need to remove null bytes at the beginning
        rbin = rbin.lstrip(b'\x00')
        ##Checking if rbin >= 0x80
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, 'big')
        ##remove null bytes as r
        sbin = sbin.lstrip(b'\x00')
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result


class S256Field(FiniteElement):#creating a field of secp256ki
    def __init__(self, element, prime=None):
        super().__init__(element=element, prime=P)

    def sqrt(self):
        """
        Here we are trying to get a square root in a finite field
        using Fermat's little theorem, P is such that P % 4 == 3,
        hence (P+1)%4 = 0, hence using fermat's little theorem
        w^2 = v when know v becomes w^2^(p+1)/4 = v^(p+1)/4
        """
        return self**((P + 1) // 4)

    def __repr__(self):
        return '{:x}'.format(self.element).zfill(64) #256bit number

class S256Point(Point):#defining the point for the field above
    def __init__(self, x, y, a=None, b=None):
        _a = S256Field(A)
        _b = S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y, P), a=_a, b=_b)
        else:
            super().__init__(x=x, y=y, a=_a, b=_b)

    def __rmul__(self, coefficient):#defining recursive multiplication as we know N
        coef = coefficient % N #to make sure that the coefficient always goes back to 0 incase bigger than N
        return super().__rmul__(coef) 
    def __repr__(self):
        return 'S256Point {}, {}'.format(self.x, self.y)

    def verify(self, Signature, z):#functioning to verify a privatekey
        s_inverse = pow(Signature.s, N-2, N) #fermat's theorem is used here
        u = z * s_inverse % N
        v = Signature.r * s_inverse % N
        a_point = (u*G + v*self) 
        return a_point.x.element == Signature.r
    def SEC(self, compressed = True):
        """
        returns compressed serialized point be default
        """
        if compressed:
            if self.y.element % 2:
                prefix_byte = b'\x02'
                x_byte = self.x.element.to_bytes(32, 'big')
            else:
                prefix_byte = b'\x03'
                x_byte = self.x.element.to_bytes(32, 'big')
            return prefix_byte + x_byte
        else:
            prefix_byte = b'\x04'
            x_byte = self.x.element.to_bytes(32, 'big')
            y_byte = self.y.element.to_bytes(32, 'big')
            return prefix_byte + x_byte + y_byte

    @classmethod
    def parse(self, sec_bin):
        """
        This method determines which to use from SEC 
        """
        if sec_bin[0] == 4:
            #not compressed
            x = int.from_bytes(sec_bin[1:33], 'big') #first 32 bytes after the marker
            y = int.from_bytes(sec_bin[33:65], 'big') #next 32 bytes after the first 32 bytes from the marker
            
            ##compressed case
            #case 1 (marker is 2)
        is_even = (sec_bin[0] == 2)
        x = S256Field(int.from_bytes(sec_bin[1:], 'big')) #remember we only get x
            ##we can use the equation to derive y
        alpha = x ** 3 + S256Field(B)
        beta = alpha.sqrt()
        if beta.element % 2:
            even_beta = beta
        else:
            even_beta = S256Field(P - beta.element)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)


    def hash160(self, compressed=True):
        return hash160(self.SEC(compressed))

    def address(self, compressed=True, testnet=False):
        """
        Returns Address String
        """
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)
G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
#above we define G, generating point for secp256ki for usability


class PrivateKey():
    def __init__(self, secret):
        self.secret = secret
        self.point = secret*G #public key is the generating point multiplied by our secret

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)
    def sign(self, z):
        k = self.deterministic(z)
        r = (k*G).x.element #x cordinate of our target
        k_inv = pow(k, N-2, N)
        s = (self.secret*r + z) * k_inv % N #from fermat's little theorem
        if s > N/2:
            s = N-2
        return Signature(r, s)

    def wif(self, compressed=True, testnet=False):
        """
        The function serializes the private key
        """
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)
    def deterministic(self, z): #aim at producing a random unique k for each signing
        k = b'\x00' *32
        v = b'\x00' *32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest() #using hash message au
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while  True:
            v = hmac.new(k, v, s256).digest()
            candidate = v.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x01', s256).digest()
            v = hmac(k, v, s256).digest()
