"""
This module represents the the transactions for Bitcoin
"""
from helper import SHA_2 #this one prevents collision
from helper import little_endian_to_int, int_to_little_endian #conversoin
from helper import encode_varint, read_varint #as named
import requests #http requests to shared nodes
import os #env variables
from script import Script
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
        tx_outs = ''
        for tx_in in self.tx_ins:
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
        result += encode_varint(len(self.tx_outs))
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

    def fee(self):
        """
        Calculates the fee using Transaction inputs
        Tx_inputs - Tx_outputs = fee
        """
        fee = 0
        for _ in self.tx_ins:
            fee += _.value(testnet=self.testnet)
        for _ in self.tx_outs:
            fee -= _.amount
        return fee

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

    def fetch_tx(self, testnet=False):
        """
        Fetches prev_tx from a TX inputs
        """
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        """
        Get the output value by looking up the Tx hash
        Remember Tx_index contains what output is spent in a transaction
        Return amount in Satoshi
        """
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        """
        Gets ScriptPubKey by looking up Tx Hash
        Returns a Script Object
        """
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

class TxOut:
    """
    A class that implements the Bitcoins Outputs
    amount - Amount in Satoshis
    script_pubkey = script_pubkey
    """
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return f"{self.amount}:{self.script_pubkey}"

    def serialize(self):
        """
        Returns byte serialization of transaction 
        output
        """
        result = int_to_little_endian(self.amount, 8)
        #bitcoin divisibility
        result += self.script_pubkey.serialize()
        #serializing the script_pubkey
        return result
    @classmethod
    def parse(cls, s):
        """
        Takes a byte stream and parses tx_output at the start
        returns a tx_out object"""
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)


class TxFetcher:
    """
    the class handles looking up the amount in inputs
    from UTXO set from a full node to calculate transaction
    fee (inputs - outputs
    """
    cache = {}

    @classmethod
    def get_url(cls, testnet = False):
        """We are utilizing a shared node
        hence there is need yo retrieve the whole transaction
        and verify the ID
        """
        if testnet:
            return f"https://go.getblock.io/{os.environ.get(TESTNET_ACCESS_TOKEN)}"
        else:
            return f"https://go.getblock.io/{os.environ.get(MAINNET_ACCESS_TOKEN)}"

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = f"{cls.get_url(testnet)}/rest/tx/{tx_id}.hex"
            response = requests.get(url)
            # the response is in bytes
            #its more compact an we also know how to
            #parse a transaction as defined in Tx
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError(f"Unexpected Response: {response.text}")
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError(f"Not Same Id: {tx.id()} != {tx_id}")

            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]

