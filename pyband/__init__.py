from .blockchain import Blockchain
from .key_manager import KeyManager


class BandProtocolClient(object):
    def __init__(self, config, abi, key):
        self.blockchain = Blockchain(config, abi)
        self.key = KeyManager(key)
