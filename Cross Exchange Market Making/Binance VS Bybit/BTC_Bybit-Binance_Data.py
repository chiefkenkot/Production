import time
import json
import pandas as pd
import requests
import os
from datetime import datetime
import re
import pal

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Replace this with your actual Binance API key
# BINANCE_API_KEY = pal.binance_key
BINANCE_API_KEY = pal.binance_key

import requests

def fetch_binance_data(symbol):
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    headers = {'X-MBX-APIKEY': pal.binance_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    target_data = None
    for item in data:
        if item['symbol'] == symbol:
            target_data = item
            break

    if target_data is None:
        raise ValueError(f'Symbol {symbol} not found in the response data.')

    ask_price = float(target_data['askPrice'])
    bid_price = float(target_data['bidPrice'])
    volume = None  # The bookTicker endpoint does not provide 24-hour trading volume.

    return ask_price, bid_price, volume


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
    volume = float(target_data['volume24h'])

    return ask_price,bid_price, volume


def fetch_and_append_data_merged():
    binance_pair = 'BTCTUSD'
    binance_ask_price, binance_bid_price, _ = fetch_binance_data(binance_pair)
    binance_ask_header = 'Binance_' + binance_pair.replace('/', '') + '_Ask'
    binance_bid_header = 'Binance_' + binance_pair.replace('/', '') + '_Bid'

    bybit_pair = 'BTCUSDC'
    bybit_ask_price, bybit_bid_price, _ = fetch_bybit_data(bybit_pair)
    bybit_ask_header = 'Bybit_' + bybit_pair + '_Ask'
    bybit_bid_header = 'Bybit_' + bybit_pair + '_Bid'

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        binance_ask_header: [binance_ask_price],
        binance_bid_header: [binance_bid_price],
        bybit_ask_header: [bybit_ask_price],
        bybit_bid_header: [bybit_bid_price],
    }

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_Bybit-Binance_Data.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

# Set an interval (in seconds)
interval = 5

while True:
    try:
        merged_data_dict = fetch_and_append_data_merged()
        time.sleep(interval)
    except Exception as e:
        print(f'Error: {e}')
        continue