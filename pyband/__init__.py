from .blockchain import Blockchain
from .key_manager import KeyManager


class BandProtocolClient(object):
    def __init__(self, endpoint, key):
        self.blockchain = Blockchain(endpoint)
        self.key = KeyManager(key)
