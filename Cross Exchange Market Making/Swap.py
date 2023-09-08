import json
import csv
import time
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# Set up the connection to the Arbitrum network
provider = HTTPProvider("https://arbitrum-mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
w3 = Web3(provider)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load the DODO contract ABI
with open("dodo_abi.json") as f:
    dodo_abi = json.load(f)

# Initialize the DODO contract with the contract address
dodo_contract_address = "DODO_CONTRACT_ADDRESS"
dodo_contract = w3.eth.contract(address=dodo_contract_address, abi=dodo_abi)

# Define the swap parameters
from_token = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"  # USDT token address
to_token = "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f"  # wBTC token address
from_token_amount = w3.toWei(100, "gwei")  # Amount of USDT to swap (100 USDT)

# Function to fetch price data
def get_price_data():
    price_data = dodo_contract.functions.querySellQuote(from_token, from_token_amount, to_token).call()
    return price_data

# Function to store price data in a CSV file
def store_price_data_in_csv(price_data):
    with open("price_data.csv", mode="a", newline="") as csvfile:
        fieldnames = ["timestamp", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write price data
        timestamp = int(time.time())
        writer.writerow({"timestamp": timestamp, "price": price_data})

# Fetch and store price data in a CSV file
price_data = get_price_data()
store_price_data_in_csv(price_data)

print("Price data successfully stored in price_data.csv")