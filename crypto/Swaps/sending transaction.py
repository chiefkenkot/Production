from web3 import Web3
import json
import time
import pal

web3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/fa54a67453ea49aca5a014cdeab6a968'))

print(web3.is_connected())

balance = web3.eth.get_balance('0x24d671b2E1AF72864fd18cFcB77F094703Acf745')

print(balance)

from_ac = '0xec794db8Ae3BFCF39330405D4F920993FeFcB0FC'
to_ac = '0x24d671b2E1AF72864fd18cFcB77F094703Acf745'

# private_key = pal.account2_pk
#
# # address1 = web3.to_checksum_address(from_ac)
# # address2 = web3.to_checksum_address(to_ac)
#
# nonce = web3.eth._get_transaction_count(from_ac)
#
# tx = {
#     'nonce': nonce,
#     'to': to_ac,
#     'value': web3.to_wei(1, 'ether'),
#     'gas': 21000,
#     # 'maxFeePerGas': web3.to_wei('500', 'gwei'),
#     # 'maxPriorityFeePerGas': web3.to_wei('10', 'gwei'),
#     'gasPrice': web3.to_wei('150', 'gwei'),
#     'chainId': 137 # for matic network
# }
# print(nonce)
# signed_tx = web3.eth.account.sign_transaction(tx, private_key)
#
# tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
# print(tx_hash)

hash = b'\xdbH\\\xc7\xda\x8cA\xddVx\xa9W\x0b\xde`\xe0]\xa3\xf0\x86Q\x02\x8d\xbdT\t\x19zR\xe2\xc4\xa1'
print(hash.hex())
