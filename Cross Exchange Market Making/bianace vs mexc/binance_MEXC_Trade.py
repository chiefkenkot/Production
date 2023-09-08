import time
import hashlib
import hmac
import requests
import json
import urllib.parse
import pal
import hmac
import hashlib
import time
import urllib
import requests
from pprint import pprint





# def get_signed_params(secret_key, params):
#     query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])
#     signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
#     return query_string + '&signature=' + signature
#
# def get_server_time():
#     endpoint = '/api/v3/time'
#     url = 'https://api.mexc.com' + endpoint
#     response = requests.get(url)
#     return response.json()['serverTime']
#
# def place_mexc_order(symbol, side, order_type, quantity, price=None, recv_window=60000):
#     base_url = 'https://api.mexc.com'
#     endpoint = '/api/v3/order'
#
#     params = {
#         'symbol': symbol,
#         'side': side,
#         'type': order_type,
#         'quantity': quantity,
#         'timestamp': get_server_time(),
#         'recvWindow': recv_window
#     }
#
#     if price:
#         params['price'] = price
#
#     signed_params = get_signed_params(API_SECRET, params)
#
#     headers = {
#         'X-MEXC-APIKEY': API_KEY,
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#
#     response = requests.post(f'{base_url}{endpoint}?{signed_params}', headers=headers)
#     return response.json()
#
# # Example usage
# response = place_mexc_order(
#     symbol='BTCUSDT',
#     side='BUY',
#     order_type='LIMIT',
#     price=float(30000),
#     quantity=float(0.001)
# )
# print(response)




# def get_mexc_symbols():
#     base_url = 'https://api.mexc.com'
#     endpoint = '/api/v3/exchangeInfo'
#
#     response = requests.get(f'{base_url}{endpoint}')
#     symbols_info = response.json()['symbols']
#     symbols = [symbol_info['symbol'] for symbol_info in symbols_info]
#     pprint(symbols)
#     return symbols
#
# # Example usage
# symbols = get_mexc_symbols()
# print(symbols)

# def get_mexc_symbols():
#     base_url = 'https://api.mexc.com'
#     endpoint = '/api/v3/exchangeInfo'
#
#     response = requests.get(f'{base_url}{endpoint}')
#     symbols_info = response.json()
#     pprint(symbols_info)
#
#
# # Example usage
# symbols = get_mexc_symbols()
# print(symbols)


###### Binance #######


def get_signed_params(secret_key, params):
    query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return query_string + '&signature=' + signature

def place_binance_order(symbol, side, order_type, quantity, price=None, time_in_force='GTC'):
    api_key = pal.binance_key
    secret_key = pal.binance_secret
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/order'

    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
        'timestamp': int(time.time() * 1000),
    }

    if price:
        params['price'] = price

    if order_type == 'LIMIT':
        params['timeInForce'] = time_in_force

    signed_params = get_signed_params(secret_key, params)

    headers = {
        'X-MBX-APIKEY': api_key
    }

    response = requests.post(f'{base_url}{endpoint}?{signed_params}', headers=headers)
    return response.json()


def binance_buy():
    symbol = 'BTCUSDT'
    side = 'BUY'  # Use 'BUY' for long and 'SELL' for short
    order_type = 'LIMIT'  # Use 'LIMIT' for limit orders
    quantity = '0.001'  # Set your desired quantity
    price = '30000'  # Set your desired price

    result = place_binance_order(symbol, side, order_type, quantity, price)
    print(json.dumps(result, indent=2))

binance_buy()

