import ed25519
import hashlib


BASE_32_LOOKUP = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def get_addr_from_hex(addr_hex):
    addr_value = 0
    for byte in bytes.fromhex(addr_hex):
        addr_value = 256 * addr_value + byte

    iban_rev_accounts = []
    for byte_idx in range(32):
        iban_rev_accounts.append(BASE_32_LOOKUP[addr_value % 32])
        addr_value //= 32

    iban_accounts = list(reversed(iban_rev_accounts))
    checksum_value = 0
    for digit in iban_accounts + ['A', 'X']:
        if '0' <= digit <= '9':
            checksum_value = checksum_value * 10 + int(digit)
        else:
            checksum_value = checksum_value * 100 + 10 + ord(digit) - ord('A')

    checksum_digits = 98 - (checksum_value * 100) % 97

    return (
        'AX' + str(checksum_digits).zfill(2) + ' ' +
        ' '.join(''.join(iban_accounts[i * 4:i * 4 + 4]) for i in range(8)))


class KeyManager(object):
    def __init__(self, key):
        if isinstance(key, str):
            key = bytes.fromhex(key)

        self.sk = ed25519.SigningKey(key)

    def get_vk(self):
        return self.sk.vk_s.hex()

    def get_addr(self):
        return hashlib.sha256(self.sk.vk_s).hexdigest()[:40]

    def get_iban_addr(self):
        return get_addr_from_hex(self.get_addr())

    def sign(self, data):
        if isinstance(data, str):
            data = bytes.fromhex(data)

        return self.sk.sign(data).hex()
