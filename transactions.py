"""
This module represents the the transactions for Bitcoin
"""
from helper import SHA_2

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
        """
        return self.hash().hex()

    def hash(self):
        """
        Binary Hash of the legacy serialization
        """
        return SHA_2(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream):
        serialized_version = stream.read(4)
