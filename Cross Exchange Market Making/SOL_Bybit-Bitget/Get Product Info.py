import requests
from pprint import pprint
import pal
from CEX_Request import ByBitRequest

######### Bitget #########
def fetch_market_data(product_type):
    url = "https://api.bitget.com/api/mix/v1/market/contracts"
    params = {"productType": product_type}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# product_type = "cmcbl"
# data = fetch_market_data(product_type)
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


print(mexc_spot_trading_pair_symbols)

######### Bybit #########

bybit_api_key = pal.bybit_key
bybit_secret_key = pal.bybit_secret
bybit_url = "https://api.bybit.com"
byrecv_window = str(5000)
bybit_request = ByBitRequest()
bybit_request.set_up(bybit_api_key,bybit_secret_key,byrecv_window,bybit_url)

response = bybit_request.get_tickers('spot')
symbol = response['result']['list']
# pprint(response)
# pprint(symbol)

# symbol['symbol']: print(symbol) for i in symbol

all_pair = [i['symbol'] for i in symbol]
USDC_pair = []
for i in all_pair:
    if 'USDC' in i:
        USDC_pair.append(i)

print(USDC_pair)

set_1 = set(mexc_spot_trading_pair_symbols)
set_2 = set(USDC_pair)

common = set_1 & set_2
common = list(common) #['BTCUSDC', 'USDCUSDT']

print(common)