"""
Implementing Bitcoin's Script Opcodes

Note::
    All Opcodes may consume 0 or more elements and push zero or more
    elements to the stack.
    - After all operations, a valid transaction must have a non-zero
    element as the top element
"""

from helper import SHA_2, hash160

def op_0(stack):
    """
    Consumes no elements 
    Pushes 0 to the stack
    """
    stack.append(0)
    return True

def op_1negate(stack):
    """
    consumes no elements
    pushes -1 to the stack
    """
    stack.append(-1)
    return True

def op_1(stack):
    """
    Consumes no elements
    pushes 1 to the stack
    """
    stack.append(1)
    return True

def 
def op_dup(stack):
    """
    OP_DUP consumes no element and pushes 1 element to the stack
    It Duplicates the top-most element of the stack
    """
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

def op_hash256(stack):
    """
    Consumes the top-most element,
    performs sha256 twice on it and pushes
    result to the stack
    """
    if len(stack) < 1:
        return False
    element = stack.pop() #consumption
    stack.append(SHA_2(element))
    return True

def op_hash160(stack):
    """
    Consumes the top-most element,
    performs hash160(sha256&ripemd160) on it and
    pushes result to stack
    """
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True

#code for op_dup is 0x76(118)
#code for op_hash256 is 0xaa(170)
#code for op_hash160 is 0xa9(169)
#code for op_0 is 0x00(0)
#code for op_1 is 0x01(1)
#code for op_16 is 0x60(96)
#code for op_add is 0x93(147)
#code for op_checksig is 0xac(172)
OP_CODE_FUNCTIONS = {118: op_dup,
                     170: op_hash256,
                     169: op_hash160}
