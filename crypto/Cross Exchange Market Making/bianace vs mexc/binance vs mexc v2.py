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

def fetch_binance_data(pair):
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/ticker/bookTicker'
    symbol = pair.replace('/', '')

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }

    params = {
        'symbol': symbol
    }

    response = requests.get(f'{base_url}{endpoint}', params=params, headers=headers)
    data = response.json()
    return float(data['askPrice']), float(data['askQty'])


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
    ask_volume = float(data['askQty'])
    return ask_price, ask_volume

def fetch_and_append_data():
    binance_pair = 'BTC/TUSD'
    binance_price, binance_volume = fetch_binance_data(binance_pair)
    binance_header = 'Binance_' + binance_pair.replace('/', '')

    mexc_pair = 'BTC/USDT'
    mexc_price, mexc_volume = fetch_mexc_data(mexc_pair)
    mexc_header = 'MEXC_' + mexc_pair.replace('/', '')

    headers = [binance_header, mexc_header]
    data = [binance_price, mexc_price]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data_dict = {'timestamp': [timestamp]}
    data_dict.update({header: [value] for header, value in zip(headers, data)})

    df = pd.DataFrame(data_dict)

    csv_file = "BTC_future_price_diff_merged_2.csv"

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

while True:
    fetch_and_append_data()
    time.sleep(1)