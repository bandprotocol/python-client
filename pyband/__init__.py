from .blockchain import Blockchain
from .key_manager import KeyManager
import requests
import json
import base64


class BandProtocolClient(object):
    def __init__(self, config, key):
        self.blockchain = Blockchain(config)
        self.key = KeyManager(key)
