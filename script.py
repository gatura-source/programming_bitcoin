"""
Both ScriptPubKey and ScriptSig are parsed the same way where if the byte is btwn
0x01 and 0x4b, it is read as an element , otherwise it is read as an operation
Op_codes are listed here for more information https://en.bitcoin.it/wiki/Script#Script_examples
Now that we know how script works and have all op_codes
We can write a script parser
"""

from helper import encode_varint, read_varint, little_endian_to_int, int_to_little_endian
class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds
    @classmethod
    def parse(cls, s):
        length = read_varint(s)
        cmds = []
        count = 0
        while count < length:
            current = s.read(1)
            count += 1
            current_byte = current[0]
            if current_byte >= 1 and current_byte <= 75:
                #We read it as an element
                n = current_byte
                cmds.append(s.read(n))
                count += n
            elif current_byte == 76:
                #OP_PUSHDATA1
                data_length = little_endian_to_int(s.read(1))
                cmds.append(s.read(data_length))
                count += data_length+1
            elif current_byte == 77:
                #OP_PUSHDATA2
                data_length = little_endian_to_int(s.read(2))
                cmds.append(s.read(data_length))
                count += data_length+2
            else:
                op_code = current_byte
                cmds.append(op_code)
        if count != length:
            print(f"Length is {length}, Count is {count}")
            #import sys
            #sys.exit(-1)
            raise SyntaxError("Parsing Script Failed")
        return cls(cmds)
    #alternatively we can also code a Script Serializer
    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                #we know its an opcode if its an int
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    #Between 1 and 75 inclusive, we encode length as a Single byte
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    #Between 76 and 255 we put OP_PUSHDATA1 first then encode length as single byte
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    #Between 256 and 520 we put OP_PUSHDATA2 first then encode length as 2 bytes in little_endian followed by the element
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    #any element longer than 520 is not valid
                    raise ValueError("Too long a cmd")
                result += cmd
        return result
    def serialize(self):
        #Any serialization starts with length of entire script
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result
