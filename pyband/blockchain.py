import base64
import json
import requests
import time
import string

from .varint import varint_encode, varint_decode
from .key_manager import KeyManager


class String(object):
    def __init__(self, name, max_length, is_sensitive):
        self.name = name
        self.max_length = max_length
        self.is_sensitive = is_sensitive

    def dump(self, value):
        if len(value) > self.max_length:
            raise Exception(
                "<{}> String's length ({}) exceeds max_length ({})".format(
                    self.name, len(value), self.max_length))

        if not all(c in string.printable for c in value):
            raise Exception(
                "<{}>There are unprintable characters in string".format(
                    self.name))

        if not self.is_sensitive and not value.islower():
            raise Exception(
                "<{}>There are upper characters in Insensitive case".format(
                    self.name))

        return varint_encode(len(value)) + value.encode()

    def parse(self, data):
        start_string = 0
        for idx, toread in enumerate(list(data)):
            if not (toread & 0x80):
                start_string = idx+1
                break
        return data[start_string:].decode()


class UnsignedInteger(object):
    def __init__(self, precision_bit, casting=int):
        self.max_value = 1 << precision_bit
        self.casting = casting

    def dump(self, value):
        value = int(value)

        if not isinstance(value, int):
            raise ValueError('{} must be an unsigned integer'.format(value))
        if value < 0 or value >= self.max_value:
            raise ValueError('Invalid unsigned integer range {}'.format(value))

        return varint_encode(value)

    def parse(self, data):
        value = varint_decode(data)
        if value >= self.max_value:
            raise ValueError('Invalid unsigned integer range')
        return self.casting(value)


class Bytes(object):
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def dump(self, value):
        if isinstance(value, str):
            value = bytes.fromhex(value)

        if len(value) != self.length:
            raise ValueError('Invalid {} length {}'.format(self.name, value))

        return value

    def parse(self, data):
        if len(data) < self.length:
            raise ValueError(
                'Unable to parse {} to {}. Too short'.format(self.name, data))

        return data[:self.length].hex()


class Equation(object):
    def __init__(self):
        self.prcd = {'+': 2, '-': 2, '*': 4, '/': 4, '%': 4, '^': 6,
                     '(': 1, ')': 1, '#': 1}

    def tokenized(self, str):
        token = []
        for ch in str.replace(' ', ''):
            if '0' <= ch <= '9':
                if token and isinstance(token[-1], int):
                    token.append(token.pop() * 10 + int(ch))
                else:
                    token.append(int(ch))
            else:
                token.append(ch)

        return token

    def infix_to_prefix(self, tokens):
        tokens.reverse()
        stack = []
        new_tokens = []
        stack.append('#')
        for token in tokens:
            if not(token in self.prcd):
                new_tokens.append(token)
            else:
                if token == ')':
                    stack.append('(')
                elif token == '(':
                    while stack[-1] != '(':
                        new_tokens.append(stack.pop())
                    stack.pop()
                else:
                    while self.prcd[stack[-1]] > self.prcd[token]:
                        new_tokens.append(stack.pop())
                    stack.append(token)

        while stack[-1] != '#':
            new_tokens.append(stack.pop())

        return list(reversed(new_tokens))

    def prefix_to_bytes(self, tokens):
        result = b''
        for token in tokens:
            if token == '+':
                result += b'\x01'
            elif token == '-':
                result += b'\x02'
            elif token == '*':
                result += b'\x03'
            elif token == '/':
                result += b'\x04'
            elif token == '%':
                result += b'\x05'
            elif token == '^':
                result += b'\x06'
            elif token == 'x':
                result += b'\x08'
            else:
                result += b'\x07'
                result += varint_encode(token)

        return result

    def bytes_to_prefix(self, data):
        tokens = []
        number = bytearray()
        in_progress = False
        for byte in data:
            if in_progress:
                number += bytes([byte])
                if not (byte & 0x80):
                    value = varint_decode(number)
                    number = b''
                    tokens.append(value)
                    in_progress = False
            else:
                if byte == 0x01:
                    tokens.append('+')
                elif byte == 0x02:
                    tokens.append('-')
                elif byte == 0x03:
                    tokens.append('*')
                elif byte == 0x04:
                    tokens.append('/')
                elif byte == 0x05:
                    tokens.append('%')
                elif byte == 0x06:
                    tokens.append('^')
                elif byte == 0x07:
                    in_progress = True
                elif byte == 0x08:
                    tokens.append('x')
                else:
                    raise ValueError('Invalid bytes string')
        return tokens

    def prefix_to_infix(self, tokens):
        stack = []
        for token in reversed(tokens):
            if token in self.prcd:
                first = stack.pop()
                second = stack.pop()
                stack.append('({} {} {})'.format(first, token, second))
            else:
                stack.append(str(token))

        return stack.pop()

    def dump(self, str):
        tokens = self.tokenized(str)
        prefix = self.infix_to_prefix(tokens)
        data = self.prefix_to_bytes(prefix)

        return data

    def parse(self, data):
        prefix = self.bytes_to_prefix(data)
        return self.prefix_to_infix(prefix)

IDENT_LOOKUP = {
    'bool': UnsignedInteger(1, bool),
    'uint8_t': UnsignedInteger(8),
    'uint16_t': UnsignedInteger(16),
    'uint32_t': UnsignedInteger(32),
    'uint64_t': UnsignedInteger(64),
    'uint256_t': UnsignedInteger(256),
    'Address': Bytes('Address', 20),
    'Hash': Bytes('Hash', 32),
    'Signature': Bytes('Signature', 64),
    'Ident': String('Ident', 20, False),
    'NodeID': String('NodeID', 128, True),
    'Curve': Equation(),
}


class Message(object):
    def __init__(self, config, name, abi_msg):
        self.config = config
        self.name = name
        self.abi_msg = abi_msg

    def __call__(self, *args, **kwargs):
        if args:
            if len(args) != 1 or not isinstance(args[0], dict):
                raise Exception(
                    "Message argument must be dictionary or keyword arguments")
            input_arg = args[0]
        else:
            input_arg = kwargs

        raw_tx = varint_encode(self.abi_msg['ID'])
        for arg in self.abi_msg['Input']:
            arg_name, arg_type = arg.split(':')
            if arg_name not in input_arg:
                raise Exception("({}) not found".format(arg_name))
            raw_tx += IDENT_LOOKUP[arg_type].dump(input_arg[arg_name])

        timestamp = self.config.clock.get_time()
        key = input_arg['key']
        tx = IDENT_LOOKUP['Ident'].dump(key.username)
        tx += bytes.fromhex(key.sign(timestamp, raw_tx))
        tx += varint_encode(timestamp) + raw_tx

        response = requests.post(self.config.endpoint, data=json.dumps({
            'jsonrpc': '2.0',
            'id': 'PYBAND',
            'method': 'broadcast_tx_commit',
            'params': {
                'tx': base64.b64encode(tx).decode('utf-8')
            }
        })).json()

        error_info = response['result']['deliver_tx'].get('info', '')
        if error_info != '':
            return error_info
        result = base64.b64decode(
            response['result']['deliver_tx'].get('data', ''))

        return result

        # for arg in self.abi_msg['Output']:
        #     arg_name, arg_type = arg.split(':')
        #     output[arg_name] = IDENT_LOOKUP[arg_type].parse(result[])
        # return IDENT_LOOKUP[self.result].parse(base64.b64decode(
        #     response['result']['deliver_tx'].get('data', '')))


class Blockchain(object):
    abi = None

    def __init__(self, config):
        if Blockchain.abi is None:
            response = requests.post(config.endpoint, data=json.dumps({
                'jsonrpc': '2.0',
                'id': 'PYBAND',
                'method': 'abci_query',
                'params': {
                    'path': 'abi'
                }
            })).json()
            Blockchain.abi = json.loads(base64.b64decode(
                response['result']['response'].get('value', '')
            ).decode('utf-8'))
        self.config = config

    def __getattr__(self, attr):
        if attr not in self.abi:
            raise KeyError('Invalid message {}'.format(attr))
        return Message(self.config, attr, self.abi[attr])
