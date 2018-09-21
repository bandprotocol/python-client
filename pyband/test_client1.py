from pyband import BandProtocolClient
from pyband.config import Config, MockClock, RealClock
from pyband.varint import varint_encode, varint_decode
import requests
import base64
import json
import hashlib


# clock = MockClock(0)

# client = BandProtocolClient(Config('http://localhost:26657/', clock),
#                             'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd')
# client2 = BandProtocolClient(Config('http://localhost:26657/', clock),
#                              '5e44d24cb81f599fbaac9d0817290aa810beac244af95f163837fedd68749633fb6fc5062d71cb56d1dff269ffb050b962c1e346b44f8eccecb673e7f88553e4')

clock = RealClock()
client = BandProtocolClient(Config('http://localhost:26657/', clock), 'e480f19604b0e44a0b65b67315c97ffac223a4e85c764a6890ac05e3047fb93878e3d3647baadde0b9e92c3bb2eca1b8b8944cf263c5ef38a7d489f8a64baedd', 'bandgod')
client.blockchain.MintToken(key=client.key, token='band', value=20)
# 480564be72759f7d5b017f09817e2a87135e07ec
creator = client.blockchain.Creator('0' * 40)
token = client.blockchain.Token('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

addr = creator.create(
    client.blockchain.Account.constructor(client.key.get_vk()))
account = client.blockchain.Account(addr)

# ct_id = creator.create(client.blockchain.Token.constructor(
#     'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('06080702')))
ct_id = creator.create(client.blockchain.Token.constructor(
    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', bytes.fromhex('06040807efabbd8ea1e8bb040704')))

ct_token = client.blockchain.Token(ct_id)

voting_id = creator.create(client.blockchain.Voting.constructor(ct_id))
vote = client.blockchain.Voting(voting_id)

gvn_id = creator.create(client.blockchain.Governance.constructor(
    ct_id, voting_id, 30, 70, 1000, 100, 100))
gvn = client.blockchain.Governance(gvn_id)
# gvn_id = '7777777777777777777777777777777777777777'

tcr_id = creator.create(client.blockchain.Registry.constructor(
    ct_id, voting_id, gvn_id, 50, 50, 100, 100, 100, 100))
tcr = client.blockchain.Registry(tcr_id)

token.mint(client.key, 1, 550000)
ct_token.buy(client.key, 2, 500)
vote.request_voting_power(client.key, 3, 100)

tcr.apply(client.key, 4, "Swit will come back to Thai!!!!", 120)


# client 2 challenge
clock.set_time(10)

addr2 = creator.create(
    client2.blockchain.Account.constructor(client2.key.get_vk()))
account2 = client.blockchain.Account(addr2)

token.mint(client2.key, 1, 1000000)
ct_token.buy(client2.key, 2, 500)
tcr.challenge(client2.key, 3, 1, "He won't come back.")
vote.request_voting_power(client2.key, 4, 1)

clock.set_time(20)
vote.commit_vote(client2.key, 5, 1, hashlib.sha256(
    b'\x00' + varint_encode(79)).digest(), 1)

clock.set_time(150)
vote.reveal_vote(client2.key, 6, 1, False, 79)

# no one vote
clock.set_time(220)
tcr.update_status(client2.key, 14, 1)

# New apply
clock.set_time(300)
tcr.apply(client.key, 5, "Swit loves kfc too much.", 200)

clock.set_time(401)
tcr.update_status(client.key, 6, 2)

clock.set_time(420)
tcr.challenge(client2.key, 15, 2, "He loves Mcdonald more.")

# Create 3 voter
clock.set_time(450)
voter1 = BandProtocolClient(Config('http://localhost:26657/', clock),
                            '7a54dc810f0a5889da9f32620c675375d63bdfebb20ac6a6669c7ed48da2c516e19d33b8365584aef2bf9a54f2d7cfbd025cc94b536dc1da04f5f05a0ceca652')
voter2 = BandProtocolClient(Config('http://localhost:26657/', clock),
                            '065fb538352b432443c0f509a7c462e903a324120d41bf972799eeec9ec37058a00e155d681fc36325b2148bf54b43841104353470fefd921f18b1b27c89cd42')
voter3 = BandProtocolClient(Config('http://localhost:26657/', clock),
                            'a5a51a0974bb2fbea0abfc68d14b9ef226f8ed2eaa98c293d173e40e221e8eabe3b7d02e3ef94c0e3d47fef2a90ba51150abd47dd34876758b5267ce265fc1b0')
voter4 = BandProtocolClient(Config('http://localhost:26657/', clock),
                            '124d043b9e8f757764bec574a2e24532663c83fadf4c9c681f9dec64521712d34a31eeee9abbbbee78f0b7cd21136b66f6e17d00c0c20e76db7d352ca188d3fc')

addrv1 = creator.create(
    voter1.blockchain.Account.constructor(voter1.key.get_vk()))
av1 = voter1.blockchain.Account(addrv1)
addrv2 = creator.create(
    voter2.blockchain.Account.constructor(voter2.key.get_vk()))
av2 = voter2.blockchain.Account(addrv2)
addrv3 = creator.create(
    voter3.blockchain.Account.constructor(voter3.key.get_vk()))
av3 = voter3.blockchain.Account(addrv3)
addrv4 = creator.create(
    voter4.blockchain.Account.constructor(voter4.key.get_vk()))
av4 = voter4.blockchain.Account(addrv4)

ct_token.mint(voter1.key, 1, 1000)
ct_token.mint(voter2.key, 1, 1000)
ct_token.mint(voter3.key, 1, 1000)
ct_token.mint(voter4.key, 1, 1000)

vote.request_voting_power(voter1.key, 2, 700)
vote.request_voting_power(voter2.key, 2, 400)
vote.request_voting_power(voter3.key, 2, 400)
vote.request_voting_power(voter4.key, 2, 200)

vote.commit_vote(voter1.key, 3, 2, hashlib.sha256(
    b'\x00' + varint_encode(79)).digest(), 700)
vote.commit_vote(voter2.key, 3, 2, hashlib.sha256(
    b'\x01' + varint_encode(434)).digest(), 400)
vote.commit_vote(voter3.key, 3, 2, hashlib.sha256(
    b'\x01' + varint_encode(178)).digest(), 400)

clock.set_time(550)
vote.commit_vote(voter4.key, 3, 2, hashlib.sha256(
    b'\x00' + varint_encode(999)).digest(), 200)
vote.reveal_vote(voter1.key, 4, 2, False, 79)

clock.set_time(600)
vote.reveal_vote(voter2.key, 4, 2, True, 434)
vote.reveal_vote(voter3.key, 4, 2, True, 178)

clock.set_time(630)
tcr.update_status(client.key, 7, 2)

ct_token.balance(addrv2)
tcr.claim_reward(voter2.key, 5, 2, 434)
ct_token.balance(addrv2)

ct_token.balance(addrv3)
tcr.claim_reward(voter3.key, 5, 2, 178)
ct_token.balance(addrv3)

vote.withdraw_voting_power(voter1.key, 5, 678)

# Deposit and withdraw stake on list
ct_token.balance(addr)
tcr.withdraw(client.key, 8, 2, 150)
ct_token.balance(addr)

ct_token.balance(addr)
tcr.deposit(client.key, 9, 2, 200)
ct_token.balance(addr)

# New list and challenge
clock.set_time(700)
tcr.apply(client2.key, 16, "I don't want to know story about Swit.", 300)

clock.set_time(750)
tcr.withdraw(client.key, 10, 2, 50)
tcr.challenge(client.key, 11, 3,
              "Swit is a famous person, everyone want to know everything about him!!")

vote.request_voting_power(voter1.key, 6, 378)

clock.set_time(800)
vote.commit_vote(voter1.key, 7, 3, hashlib.sha256(
    b'\x01' + varint_encode(1476)).digest(), 400)
vote.commit_vote(voter2.key, 6, 3, hashlib.sha256(
    b'\x01' + varint_encode(5810)).digest(), 400)
vote.commit_vote(voter3.key, 6, 3, hashlib.sha256(
    b'\x00' + varint_encode(7223)).digest(), 400)
vote.commit_vote(voter4.key, 3, 3, hashlib.sha256(
    b'\x00' + varint_encode(9875)).digest(), 200)

clock.set_time(900)
vote.reveal_vote(voter1.key, 8, 3, True, 1476)
vote.reveal_vote(voter3.key, 7, 3, False, 7223)
vote.reveal_vote(voter4.key, 4, 3, False, 9875)

# voter 1 want token can withdraw because reveal vote already
clock.set_time(914)
vote.withdraw_voting_power(voter1.key, 9, 300)

# too late!
clock.set_time(951)
vote.reveal_vote(voter2.key, 7, 3, True, 5810)

# addr1 update status want to beat challenge(remove list)
tcr.update_status(client.key, 12, 3)

ct_token.balance(addr)  # 150

# Voter 2 want to withdraw vote
vote.withdraw_voting_power(voter2.key, 7, 300)

vote.rescue_token(voter2.key, 7, 3)

# Voter 2 can withdraw now
vote.withdraw_voting_power(voter2.key, 8, 400)

# voter 3 and 4 claim reward
ct_token.balance(addrv3)  # 625
tcr.claim_reward(voter3.key, 8, 3, 7223)
ct_token.balance(addrv3)  # 658

ct_token.balance(addrv4)  # 800
tcr.claim_reward(voter4.key, 5, 3, 9875)
ct_token.balance(addrv4)  # 817

ct_token.balance(addr)  # 150
tcr.exit(client.key, 13, 2)
ct_token.balance(addr)  # 400


import threading
import time


def f():
    time.sleep(1)
    print('hey')


for i in range(10):
    threading.Thread(target=f).start()
