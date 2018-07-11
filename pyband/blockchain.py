import base64
import json
import requests


class Blockchain(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def abci_query(self, method, **params):
        response = requests.post(self.endpoint, data=json.dumps({
            'jsonrpc': '2.0',
            'id': 'PYBAND',
            'method': 'abci_query',
            'params': {
                'data': json.dumps({
                    'method': method,
                    'params': params,
                }).encode().hex()
            }
        })).json()

        return json.loads(
            base64.b64decode(response['result']['response']['value']))

    def broadcast_tx_commit(self, tx):
        if isinstance(tx, str):
            tx = bytes.fromhex(tx)

        response = requests.post(self.endpoint, data=json.dumps({
            'jsonrpc': '2.0',
            'id': 'PYBAND',
            'method': 'broadcast_tx_commit',
            'params': {
                'tx': base64.b64encode(tx).decode('utf-8')
            }
        })).json()

        return response
