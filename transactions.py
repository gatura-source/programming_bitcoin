"""
This module represents the the transactions for Bitcoin
"""
from helper import SHA_2
from helper import little_endian_to_int, int_to_little_endian
from helper import encode_varint, read_varint

class Tx:
    """
    Module represents bitcoin transactions
    """
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        #indicates what additional features the transaction uses
        
        self.tx_ins = tx_ins
        #what bitcoins are being spent

        self.tx_outs = tx_outs
        #where bitcoins are going

        self.locktime = locktime
        #when bitcoin will be spendable

        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_ins in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return f"tx: {self.id()}\nversion: {self.version}\ntx_ins:\n{tx_ins}\ntx_outs:\n{tx_outs}\nlocktime: {self.locktime}"

    def id(self):
        """
        Human-readable hexadecimal of the transaction hash
        Transaction ID
        """
        return self.hash().hex()

    def hash(self):
        """
        Binary Hash of the legacy serialization
        """
        return SHA_2(self.serialize())[::-1]

    def serialize(self):
        """
        Returns the byte serialization of transaction
        """
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self_tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result
    @classmethod
    def parse(cls, stream, testnet=False):
        """Parsing a transaction"""
        version = little_endian_to_int(stream.read(4))
        num_inputs = read_varint(stream)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))

        num_outputs = read_varint(stream)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(stream))
        locktime = little_endian_to_int(stream.read(4))
        return cls(version, inputs, outputs, locktime, testnet=testnet)
class TxIn:
    """
    A class that implements the inputs of a Bitcoin transaction
    
    prev_tx - previous tx ID
    prev_index - prevoius tx Index
    ScriptSig - bitcoins Smart Contract language Script
    Sequence  - High-Freq trade
    """
    def __init__(self, prev_tx, prev_index, script_sig=None,
                 sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence


    def __repr__(self):
        return f"{self.prev_tx.hex()}:{self.prev_index}"

    def serialize(self):
        """
        Returns byte serialization of the transaction input
        """
        result = self.prev_tx[::-1] #this is because prev_tx is little-endian hence reversing it has same effect as int_to_little_endian
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result
    @classmethod
    def parse(cls, s):
        """
        Takes a byte stream and parses tx_input at the start
        returns a tx_in object
        """
        prev_tx = s.read(32)[::1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig = Script.parse(s)
        sequence = little_endian_to_int(s.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

class TxOut:
    """
    A class that implements the Bitcoins Outputs
    amount - Amount in Satoshis
    script_pubkey = script_pubkey
    """
    def __init__(self, amout, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return f"{self.amount}:{self.script_pubkey}"

    @classmethod
    def parse(cls, s):
        """
        Takes a byte stream and parses tx_output at the start
        returns a tx_out object"""
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)




