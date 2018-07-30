import base64
import json
import requests

from .varint import varint_encode, varint_decode
from .key_manager import KeyManager


class Void(object):
    def dump(self, value):
        return b''

    def parse(self, data):
        return None


class Buffer(object):
    def dump(self, value):
        return value

    def parse(self, data):
        return data


class UnsignedInteger(object):
    def __init__(self, precision_bit, casting=int):
        self.max_value = 1 << precision_bit
        self.casting = casting

    def dump(self, value):
        value = int(value)

        if not isinstance(value, int):
            raise ValueError("{} must be an unsigned integer".format(value))
        if value < 0 or value >= self.max_value:
            raise ValueError("Invalid unsigned integer range {}".format(value))

        return varint_encode(value)

    def parse(self, data):
        value = varint_decode(data)
        if value >= self.max_value:
            raise ValueError("Invalid unsigned integer range")
        return self.casting(value)


class Bytes(object):
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def dump(self, value):
        if isinstance(value, str):
            value = bytes.fromhex(value)

        if len(value) != self.length:
            raise ValueError("Invalid {} length {}".format(self.name, value))

        return value

    def parse(self, data):
        if len(data) < self.length:
            raise ValueError(
                "Unable to parse {} to {}. Too short".format(self.name, data))

        return data[:self.length].hex()


IDENT_LOOKUP = {
    'void': Void(),
    'bool': UnsignedInteger(1, bool),
    'uint8_t': UnsignedInteger(8),
    'uint16_t': UnsignedInteger(16),
    'uint32_t': UnsignedInteger(32),
    'uint64_t': UnsignedInteger(64),
    'uint256_t': UnsignedInteger(256),
    'Address': Bytes('Address', 20),
    'Hash': Bytes('Hash', 32),
    'Signature': Bytes('Signature', 64),
    'Buffer': Buffer(),
}


class Function(object):
    def __init__(self, endpoint, name, addr, opcode, params, result):
        self.endpoint = endpoint
        self.name = name
        self.tx_prefix = addr + IDENT_LOOKUP['uint16_t'].dump(opcode)
        self.params = params
        self.result = result

    def raw_tx(self, *args):
        if len(self.params) != len(args):
            raise ValueError(
                "Invalid number of arguments to {}".format(self.name))

        tx_data = self.tx_prefix
        for idx in range(len(args)):
            tx_data += IDENT_LOOKUP[self.params[idx]].dump(args[idx])

        return tx_data

    def __call__(self, *args):
        if len(args) >= 2 and isinstance (args[0], KeyManager) and isinstance (args[1], int):
            tx_data = bytes.fromhex(args[0].sign(args[1], self.raw_tx(*args[2:])))
        else:
            tx_data = self.raw_tx(*args)

        # TODO:
        timestamp = varint_encode(10)

        response = requests.post(self.endpoint, data=json.dumps({
            'jsonrpc': '2.0',
            'id': 'PYBAND',
            'method': 'broadcast_tx_commit',
            'params': {
                'tx': base64.b64encode(timestamp + tx_data).decode('utf-8')
            }
        })).json()

        return response


class Contract(object):
    def __init__(self, endpoint, name, addr, abi_contract):
        self.endpoint = endpoint
        self.name = name
        self.addr = IDENT_LOOKUP['Address'].dump(addr)
        self.abi_contract = abi_contract

    def __getattr__(self, attr):
        if attr not in self.abi_contract:
            raise KeyError("Invalid method {}.{}".format(self.name, attr))
        return Function(
            self.endpoint, self.name + '.' + attr, self.addr,
            **self.abi_contract[attr])


class Blockchain(object):
    def __init__(self, endpoint, abi):
        self.endpoint = endpoint
        self.abi = abi

    def __getattr__(self, attr):
        def wrap(addr):
            if attr not in self.abi:
                raise KeyError("Invalid contract {}".format(attr))
            return Contract(self.endpoint, attr, addr, self.abi[attr])
        return wrap
