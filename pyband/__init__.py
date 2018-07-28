from .blockchain import Blockchain
from .key_manager import KeyManager


class BandProtocolClient(object):
    def __init__(self, endpoint, abi, key):
        self.blockchain = Blockchain(endpoint, abi)
        self.key = KeyManager(key)
