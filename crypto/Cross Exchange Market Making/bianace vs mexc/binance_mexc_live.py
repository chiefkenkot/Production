import time
import hashlib
import hmac
import requests
import json
import pal

def get_signed_params(secret_key, params):
    query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def place_mexc_order(symbol, side, quantity, price=None):
    api_key = pal.mexc_key
    secret_key = pal.mexc_secret
    base_url = 'https://www.mxc.ceo'
    endpoint = '/open/api/v3/order/create'

    params = {
        'api_key': api_key,
        'req_time': int(time.time() * 1000),
        'symbol': symbol,
        'quantity': quantity,
        'trade_type': side
    }

    if price:
        params['price'] = price

    signature = get_signed_params(secret_key, params)
    params['sign'] = signature

    response = requests.post(f'{base_url}{endpoint}', data=params)
    return response.json()

def place_binance_order(symbol, side, order_type, quantity, price=None):
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

    signature = get_signed_params(secret_key, params)
    params['signature'] = signature

    headers = {
        'X-MBX-APIKEY': api_key
    }

    response = requests.post(f'{base_url}{endpoint}', data=params, headers=headers)
    return response.json()

def buy_order_binance():
    quantity = '0.004'
    price = '30100'

    # Binance market buy order
    binance_result = place_binance_order('BTCUSDT', 'BUY', 'LIMIT', quantity, price)
    print(json.dumps(binance_result, indent=2))


buy_order_binance()

def buy_order_mexc():
    quantity = '0.004'

    # MXC market sell order
    mexc_result = place_mexc_order('BTC_USDT', 'ASK', quantity)
    print(json.dumps(mexc_result, indent=2))

