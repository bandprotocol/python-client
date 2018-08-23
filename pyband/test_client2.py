from pyband import BandProtocolClient
from pyband.config import Config, MockClock, RealClock
from pyband.varint import varint_encode, varint_decode
from pyband.abi import abi
import base64
import hashlib
import threading
import time

clock = RealClock()

client = []

client.append(BandProtocolClient(Config('http://localhost:26657/', clock), abi,
                         'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd'))
client.append(BandProtocolClient(Config('http://localhost:26657/', clock), abi,
                         '5e44d24cb81f599fbaac9d0817290aa810beac244af95f163837fedd68749633fb6fc5062d71cb56d1dff269ffb050b962c1e346b44f8eccecb673e7f88553e4'))
client.append(BandProtocolClient(Config('http://localhost:26657/', clock), abi,
                         '23da6dee018f92bdca09db5e31b1025c6601cd93907a9e9b1c4a0b967454c136c97863497aec2511ec368f8d76922cfe24f8904f68304e4812a83a6b6a0f43f4'))
client.append(BandProtocolClient(Config('http://localhost:26657/', clock), abi,
                         '917e31255a41f110ff19f0d349a61d7cbecbc7b11852640edf26af15ae87e0e532652546a8817c1612d954655f27125fb0546947594eb5ee9483a42e5964dea2'))
client.append(BandProtocolClient(Config('http://localhost:26657/', clock), abi,'9e93c48ea256d8a6ac7dcaae47f179b7c28ba9b6a04ffff69446855570f55b9a79c7cc7c2d8033291c67b5e3cab4054a3da26adc9916145080cab4f46cb37c3c'))

addr = []

creator = client[0].blockchain.Creator('0' * 40)
token = client[0].blockchain.Token('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')


# # account = client[0].blockchain.Account(addr)
# ct_id = creator.create(client[0].blockchain.Token.constructor('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('06080702')))
# # ct_id = creator.create(client[0].blockchain.Token.constructor(
# #     'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('06040807efabbd8ea1e8bb040704')))

# ct_token = client[0].blockchain.Token(ct_id)

# voting_id = creator.create(client[0].blockchain.Voting.constructor(ct_id))
# vote = client[0].blockchain.Voting(voting_id)

# gvn_id = creator.create(client[0].blockchain.Governance.constructor(ct_id, voting_id, 30, 70, 1000, 100, 100))
# gvn = client[0].blockchain.Governance(gvn_id)
#     # gvn_id = '7777777777777777777777777777777777777777'

# tcr_id = creator.create(client[0].blockchain.Registry.constructor(ct_id, voting_id, gvn_id, 50, 50, 100, 100, 100, 100))
# tcr = client[0].blockchain.Registry(tcr_id)


def create_account(idx):
    return creator.create(client[idx].blockchain.Account.constructor(client[idx].key.get_vk()))

def mint_band(idx, val):
    token.mint(client[idx].key , clock.get_time(), val)

def print_balance(idx , name):
    print("Name : {} have {}".format(name,token.balance(addr[idx])))

def transfer(sender, receipt, val):
    token.transfer(client[sender].key, clock.get_time(), addr[receipt], val)


# for i in range(5):
#     threading.Thread(target = f, args = (i)).start()

for i in range(5):
    addr.append(create_account(i))

for i in range(5):
    threading.Thread(target=mint_band, args=(i, 1000)).start()

time.sleep(1)

for i in range(5):
    threading.Thread(target=transfer, args=(i, (i+1) % 5, i*100)).start()
    threading.Thread(target=print_balance, args=(i , "P"+str(i))).start()

time.sleep(1)

for i in range(5):
    threading.Thread(target=print_balance, args=(i, "P"+str(i))).start()
