import time
import json
import pandas as pd
import requests
import os
from datetime import datetime
import ccxt
import pal
from pprint import pprint


# GET /api/v3/defaultSymbols
# 该API返回的数据都是支持限价订单的。
# GET /api/v3/exchangeInfo
# 如果API返回字段 "isSpotTradingAllowed "为真，并且 "orderTypes "包含 "MARKET"，这意味着支持市场订单。

###### Full Data ######
# base_url = 'https://api.mexc.com'
# endpoint = '/api/v3/exchangeInfo'
#
# headers = {
#     'api_key': pal.mexc_key
# }
#
# response = requests.get(f'{base_url}{endpoint}', headers=headers)
# data = response.json()
#
# spot_trading_pairs = [pair for pair in data['symbols'] if pair['isSpotTradingAllowed']]
#
# pprint(spot_trading_pairs)

###### Market Order Pairs ######

base_url = 'https://api.mexc.com'
endpoint = '/api/v3/exchangeInfo'

headers = {
    'api_key': pal.mexc_key
}

response = requests.get(f'{base_url}{endpoint}', headers=headers)
data = response.json()

desired_order_types = {'LIMIT', 'MARKET', 'LIMIT_MAKER'}

spot_trading_pair_symbols = [
    pair['symbol'] for pair in data['symbols']
    if pair['isSpotTradingAllowed'] and set(pair['orderTypes']) == desired_order_types
]

pprint(spot_trading_pair_symbols)