import socket
import time
import json
import pandas as pd
import requests
import os
from datetime import datetime
import ccxt
import pal

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Replace these with your actual Binance and MEXC API keys
BINANCE_API_KEY = pal.binance_key
MEXC_API_KEY = pal.mexc_key

def fetch_bybit_data(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {'category': 'spot'}
    response = requests.get(url, params=params)
    data = response.json()

    # Find the target symbol in the response data
    target_data = None
    for item in data['result']['list']:
        if item['symbol'] == symbol:
            target_data = item
            break

    if target_data is None:
        raise ValueError(f'Symbol {symbol} not found in the response data.')

    ask_price = float(target_data['ask1Price'])
    bid_price = float(target_data['bid1Price'])
    # print(ask_price)
    # volume = float(target_data['volume24h'])

    return ask_price,bid_price



def fetch_mexc_data(pair):
    base_url = 'https://api.mexc.com'
    endpoint = '/api/v3/ticker/bookTicker'
    symbol = pair.replace('/', '')

    headers = {
        'api_key': MEXC_API_KEY
    }

    params = {
        'symbol': symbol
    }

    response = requests.get(f'{base_url}{endpoint}', params=params, headers=headers)
    data = response.json()

    if 'askPrice' not in data or 'askQty' not in data:
        print(f"Unexpected JSON structure from MEXC API: {data}")
        return None, None

    ask_price = float(data['askPrice'])
    bid_price = float(data['bidPrice'])
    # print(f'mexc {ask_price}ask_price')
    # ask_volume = float(data['askQty'])
    return ask_price, bid_price

# fetch_mexc_data('BTC/USDT')
# time.sleep(1234)

def fetch_and_append_data():
    bybit_pair = 'BTCUSDC'
    bybit_ask_price, bybit_bid_price = fetch_bybit_data(bybit_pair)
    bybit_ask_header = 'Bybit_' + bybit_pair + '_Ask'
    bybit_bid_header = 'Bybit_' + bybit_pair + '_Bid'

    mexc_pair = 'BTC/USDT'
    mexc_ask, mexc_bid = fetch_mexc_data(mexc_pair)
    mexc_ask_header = 'MEXC_' + mexc_pair + '_Ask'
    mexc_bid_header = 'MEXC_' + mexc_pair + '_Bid'

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        mexc_ask_header: [mexc_ask],
        mexc_bid_header: [mexc_bid],
        bybit_ask_header: [bybit_ask_price],
        bybit_bid_header: [bybit_bid_price],
    }

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_Bybit-MEXC_Data.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

while True:
    try:
        fetch_and_append_data()
        time.sleep(1)
    except (ConnectionError, socket.error):
        continue
