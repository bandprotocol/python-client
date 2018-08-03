Band Protocol Python Library
============================

Install
-------
(pip install coming soon)
```
$ git clone https://github.com/bandprotocol/python-client.git
$ cd python-client
$ python3 -m venv
$ source venv/bin/activate
$ pip install -r requirements.txt

```

Basic Usage
-----
```
$ source venv/bin/activate
$ python
>>> from pyband import BandProtocolClient
>>> from pyband.config import Config, RealClock
>>> from pyband.abi import abi
>>> clock = RealClock()
>>> secret_key = 'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd'
>>> client = BandProtocolClient(Config('http://localhost:26657/', clock), abi, secret_key)
```
### Contract
Every thing on chain is contracts, so every transaction need to know address of contract to send transaction. This library provides contract view to call function to create and send transaction to chain including generate signature of transaction by your provided secret_key.

Contract view can declare like this
```
>>> view = client.blockchain.<Contract type>(<Address of contract>)
```

Replace <<Contract type> and <Address of contract> with type of contract eg. Creator, Account. and hex address string.

#### Creater
Contract to create other contract has only 1 function create. If contract creating success, it will return address of new contract.
```
>>> creator = client.blockchain.Creator('0' * 40)
>>> addr = creator.create(client.blockchain.Account.constructor(client.key.get_vk())) 
>>> account = client.blockchain.Account(addr)
```
Every contract (except Creator) have constructor function to create raw_tx to create contract in chain. Input parameter for each contract define at abi file (constructor_params) for each contract.

#### Account
View of account contract

#### Token
View of token contract have function to manage token eg. transfaer, buy, sell token.
```
>>> ct_id = creator.create(client.blockchain.Token.constructor('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('06080702')))
>>> ct_token = client.blockchain.Token(ct_id)

>>> token.mint(client.key,0,1000)
>>> ct_token.buy(client.key,1, 10)

>>> token.balance(addr)
900
>>> ct_token.balance(addr)
10
```

#### Voting
View of voting contract have function to request vote power, commit vote, reveal vote etc.

#### Registry
View of REgistry contract have function to apply application, challenge application, reward claim for winning voter, etc.
ABI
---
Interface of every transaction that you can send to chain store in pyband/abi.py file

Demo code
---------
pyband/test_client1.py you can copy code from this file and paste on terminal. If you want to run a file.
```python test_client1.py``` please change file location to top level of pyband or edit import in file to match what script file location.
