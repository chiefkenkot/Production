import requests
import json

# def get_btc_price():
#     url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
#     query = """
#     {
#       pairs(where: {token0: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", token1: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"}) {
#         token0Price
#         token1Price
#       }
#     }
#     """
#     response = requests.post(url, json={'query': query})
#     data = json.loads(response.content)
#     btc_price = data['data']['pairs'][0]['token1Price']
#     return btc_price
#
# get_btc_price()

url = 'https://api.dodoex.io/swap_data/pairs'
response = requests.get(url)

response = response.json()
print(response)