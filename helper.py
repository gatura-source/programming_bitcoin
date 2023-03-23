import hashlib
def SHA_2(arg):
	return hashlib.sha256(hashlib.sha256(arg).digest()).digest()
	#double SHA256 used to sign the message to avoid a birthday conflict
