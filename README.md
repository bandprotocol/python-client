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
>>> from pyband.config import Config, RealClock
>>> abi = (abi interface from blockchain)
>>> clock = RealClock()
>>> client = BandProtocolClient(Config('http://localhost:26657/', clock), abi, 'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd')

>>> creator = client.blockchain.Creator('0' * 40)
>>> addr = creator.create(client.blockchain.Account.constructor(client.key.get_vk())) # Create account contract in chain
>>> account = client.blockchain.Account(addr)

>>> ct_id = creator.create(client.blockchain.Token.constructor('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('01080706')))
>>> ct_token = client.blockchain.Token(ct_id)

>>> token.mint(client.key,0,1000)
>>> ct_token.buy(client.key,1, 500)

>>> token.balance(addr)
500
