"""This is a new a script for the blockchain project as the previous one had too many errors and i could not trace them"""
class FiniteElement():
	
	def __init__(self, element, prime):
		"""Checks if the element is in the given field"""
		try:
			element < prime and element > 0
		except:
			error = f"Element not in the range 0 and {prime - 1}"
			raise ValueError(error)
		self.element = element
		self.prime = prime

	"""repr func"""
	def __repr__(self):
		return f"FiniteElement {self.element}_{self.prime}"


	"""checks for equality"""
	def __eq__(self, other):
		if other is None:
			return self
		return self.element == other.element and self.prime == other.prime


	"""does opposite of the func above"""
	def __ne__(self, other):
		return not (self == other)


	"""Element addition"""
	def __add__(self, other):
		if self.prime != other.prime:
			e = "Cannot add two Finite field elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element + other.element) % self.prime
		return self.__class__(element, self.prime)


	"""Element subtraction"""
	def __sub__(self, other):
		if self.prime != other.prime:
			e = "Cannot subtract elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element - other.element) % self.prime
		return self.__class__(element, self.prime)

	"""Element multiplaction"""
	def __mul__(self, other):
		if self.prime != other.prime:
			e = "Cannot Multiply elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element * other.element) % self.prime
		return self.__class__(element, self.prime)


	"""Element exponention"""
	def __pow__(self, exponent):
		n = exponent % (self.prime -1)
		element = pow(self.element, n, self.prime)
		return self.__class__(element, self.prime)


	"""Element division"""
	def __truediv__(self, other):
		if self.prime != other.prime:
			e = "Cannot divide not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element * pow(self.element, self.prime-2)) % self.prime
		return self.__class__(element, self.prime)

""" This class initiates a point using a polynomial function y^2 = X^3 a.x^2 + b"""
class Point():


	def __init__(self, x, y, a, b):
		self.x = x
		self.y = y
		self.a = a
		self.b = b
		if (self.y ** 2) != (self.x ** 3) + (a*x) + b:
			e = f'Point {self} is not on the curve'
			raise ValueError(e)
	def __eq__(self, other):
		if other == None:
			return False
		return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

	def __ne__(self, other):
		if other is None:
			return False
		return not self == other

	def __add__(self, other):
		if self.a != other.a and self.b != other.b:
			e = f'Point {self} and {other} are not on the same curve'
			raise TypeError(e)


		"""Point addition when y1 != y2"""
		if self.x == other.x and self.y != other.y:
			x = None
			y = None


		"""point addition when self is None"""
		if self.x is None:
			return other


		"""point addition when other is None"""
		if other.x is None:
			return self



		"""Point Addition when self.x != other.x"""
		if self.x != other.x:
			slope = (other.y - self.y) / (other.x - self.x)
			x3 = pow(slope, 2) - self.x - other.x
			y3 = (slope * (self.x - x3)) - self.y
			x = x3
			y = y3


		"""Point addition when self == other """
		if self == other:
			slope = ((3 * pow(self.x, 2)) + self.a) / (2*self.y)
			x3 = pow(slope, 2) - (2*self.y)
			y3 = slope(self.x - x3) - self.y
			x = x3
			y = y3

		"""point addition when self.y == 0(results with a zerodivision error for slope)"""
		if self == other and self.y == 0:
			x = None
			y = None
		return self.__class__(x, y, self.a, self.b)


	def __repr__(self):
		if self.x is None and self.y is None:
			return 'point infinity'
		else:
			return f'Point ({self.x}, {self.y})_{self.a} {self.b}'


P = (2 ** 256) - (2 ** 32) - 977 # prime of the field as used in secp256ki
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 #order of mathematical group generated by S256Point
A = 0 #the value used for a in secp256ki
B = 7 # the value of b as in secp256ki

class S256Field(FiniteElement):
	"""This class represents the Finite Field under which the elliptic curve falls using secp256ki"""
	def __init__(self, element, prime = None):
		super.__init__(element=element, prime=P)

	def __repr__(self):
		return '{:x}'.format((self.element).zfill(64))


class S256Point(Point):
	"""This class defines point using the scep256ki equation y^2 = x^3 + 7"""
	def __init__(x, y, a, b):
		a = S256Field(a)
		b = S256Field(b)
		super.__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)

	def __repr__(self):
		return f'S256Point_{self.x}_{self.y}'


