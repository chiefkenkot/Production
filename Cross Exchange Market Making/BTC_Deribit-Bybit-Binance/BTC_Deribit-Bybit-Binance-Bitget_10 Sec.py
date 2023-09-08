import requests

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
    volume = None  # The bookTicker endpoint does not provide 24-hour trading volume.

    return ask_price, volume


def fetch_bybit_data(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {'category': 'linear'}
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
    volume = float(target_data['volume24h'])

    return ask_price, volume

def fetch_deribit_data(symbol):
    url = f'https://www.deribit.com/api/v2/public/get_order_book?instrument_name={symbol}&depth=1'
    response = requests.get(url)
    data = response.json()

    ask_price = float(data['result']['asks'][0][0])
    volume = float(data['result']['stats']['volume'])

    return ask_price, volume


def fetch_bitget_data(symbol):
    url = "https://api.bitget.com/api/mix/v1/market/ticker"
    querystring = {"symbol": symbol}

    response = requests.get(url, params=querystring)
    data = response.json()

    if data["code"] == "00000" and "data" in data:
        target_data = data["data"]
    else:
        raise ValueError(f'Symbol {symbol} not found in the response data.')

    ask_price = float(target_data["bestAsk"])
    volume = float(target_data["usdtVolume"])

    return ask_price, volume


def fetch_and_append_data_merged():
    binance_pair = 'BTCTUSD'
    binance_price, _ = fetch_binance_data(binance_pair)
    binance_header = 'Binance_' + binance_pair.replace('/', '')

    bybit_pair = 'BTCUSDT'
    bybit_price, _ = fetch_bybit_data(bybit_pair)
    bybit_header = 'Bybit_' + bybit_pair

    deribit_pair = 'BTC-PERPETUAL'
    deribit_price, _ = fetch_deribit_data(deribit_pair)
    deribit_header = 'Deribit_' + deribit_pair.replace('-', '')

    bitget_pair = 'BTCUSDT_UMCBL'
    bitget_price, _ = fetch_bitget_data(bitget_pair)
    bitget_header = 'Bitget_' + bitget_pair.replace('_', '')

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        binance_header: [binance_price],
        bybit_header: [bybit_price],
        deribit_header: [deribit_price],
        bitget_header: [bitget_price]
    }

    df = pd.DataFrame(data_dict)

    csv_file = "BTC_Deribit-Bybit-Binance-Bitget - 10 Sec.csv"

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

interval = 10

while True:
    try:
        merged_data_dict = fetch_and_append_data_merged()
        time.sleep(interval)
    except Exception as e:
        print(f'Error: {e}')
        continue