from web3 import Web3
import json

BSC_RPC_URL = 'https://bsc.YOUR_RPC_ENDPOINT_HERE.com'
w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

ROUTER_ADDRESS = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
ROUTER_ABI_FILE = 'path/to/IPancakeRouter02.json'



with open(ROUTER_ABI_FILE) as f:
    ROUTER_ABI = json.load(f)

router_contract = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)