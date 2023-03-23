"""This is a new a script for the blockchain project as the previous one had too many errors and i could not trace them"""
class FiniteElement():
	
	def __init__(self, element, prime):
		try:
			element < prime and element > 0
		except:
			error = f"Element not in the range 0 and {prime - 1}"
			raise ValueError(error)
		self.element = element
		self.prime = prime
	def __repr__(self):
		return f"FiniteElement {self.element}_{self.prime}"

	def __eq__(self, other):
		if other is None:
			return self
		return self.element == other.element and self.prime == other.prime

	def __ne__(self, other):
		return not (self == other)

	def __add__(self, other):
		if self.prime != other.prime:
			e = "Cannot add two Finite field elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element + other.element) % self.prime
		return self.__class__(element, self.prime)
	def __sub__(self, other):
		if self.prime != other.prime:
			e = "Cannot subtract elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element - other.element) % self.prime
		return self.__class__(element, self.prime)
	def __mul__(self, other):
		if self.prime != other.prime:
			e = "Cannot Multiply elements not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element * other.element) % self.prime
		return self.__class__(element, self.prime)
	def __pow__(self, exponent):
		n = exponent % (self.prime -1)
		element = (self.element, n, self.prime)
		return self.__class__(element, self.prime)

	def __truediv__(self, other):
		if self.prime != other.prime:
			e = "Cannot divide not in the same field"
			raise TypeError(e)
		elif self.prime == other.prime:
			element = (self.element * pow(self.element, self.prime-2)) % self.prime
		return self.__class__(element, self.prime)