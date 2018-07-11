Pyband
======

Install
-------
(pip install coming soon)
```
$ git clone https://github.com/bandprotocol/python-client.git
$ cd python-client
$ python3 -m venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python
```

Usage
-----

```
>>> from pyband import BandProtocolClient
>>> client = BandProtocolClient('http://localhost:26657/', 'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd')
>>> client.key.get_addr()
'AX85 KACY KRVU QYRZ 4Y2B R6E2 C9TL S6KX 6B9N'
>>> client.blockchain.abci_query('txgen', msgid='1', vk=client.key.get_vk(), token='BX63 AAAA AAAA AAAA AAAA AAAA AAAA AAAA AAAA', value='200')
{'tx': '01e6b5cfc3c82c78e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd0000000000000000000000000000000000000000c801'}
>>> msg = client.key.sign('01e6b5cfc3c82c78e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd0000000000000000000000000000000000000000c801')
>>> client.blockchain.broadcast_tx_commit(msg)
{'jsonrpc': '2.0', 'id': 'PYBAND', 'result': {'check_tx': {'fee': {}}, 'deliver_tx': {'fee': {}}, 'hash': 'D6AB18E29B8CFFE3417F53C132A793ADA57D4AF5', 'height': 3}}
```
