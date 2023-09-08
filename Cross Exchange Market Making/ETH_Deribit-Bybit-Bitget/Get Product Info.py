import time

import requests
from pprint import pprint
import pal
from CEX_Request_V2 import ByBitRequest

######### Bitget #########
def fetch_market_data(product_type):
    url = "https://api.bitget.com/api/mix/v1/market/contracts"
    params = {"productType": product_type}

    response = requests.get(url, params=params)
    response = response.json()
    list = response['data']
    symbol = []
    for i in list:
        symbol.append(i['symbolName'])

    return symbol

product_type = "umcbl"
bitget_symbol = fetch_market_data(product_type)
# pprint(data)

######### MEXC #########
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

mexc_spot_trading_pair_symbols = [
    pair['symbol'] for pair in data['symbols']
    if pair['isSpotTradingAllowed'] and set(pair['orderTypes']) == desired_order_types
]



######### Bybit #########

bybit_api_key = pal.bybit_key
bybit_api_secret = pal.bybit_secret
bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)

response = bybit_request.get_tickers('spot')
symbol = response['result']['list']
# pprint(response)
# pprint(symbol)

# symbol['symbol']: print(symbol) for i in symbol

all_pair = [i['symbol'] for i in symbol]
USDC_pair = []
for i in all_pair:
    # if 'USDC' in i or 'USDT' in i:
    if 'USDC' in i:
        USDC_pair.append(i)


###### Compare ######
# print(f'Bitget: {bitget_symbol}')
print(f'MEXC: {mexc_spot_trading_pair_symbols}')
# print(f'Bybit: {USDC_pair}')

time.sleep(1234)
basecoins = ['USDT', 'USDC']

bitget_symbol = [s.replace(coin, '') for s in bitget_symbol for coin in basecoins if coin in s]
mexc_spot_trading_pair_symbols = [s.replace(coin, '') for s in mexc_spot_trading_pair_symbols for coin in basecoins if coin in s]
USDC_pair = [s.replace(coin, '') for s in USDC_pair for coin in basecoins if coin in s]

# print(f'Bitget: {bitget_symbol}')
# print(f'MEXC: {mexc_spot_trading_pair_symbols}')
# print(f'Bybit: {USDC_pair}')

set_1 = set(mexc_spot_trading_pair_symbols)
# set_2 = set(USDC_pair)
set_3 = set(bitget_symbol)

common = set_1 & set_3
common = list(common) #['SUI']

print(f'Common: {common}')


###### Testing ######