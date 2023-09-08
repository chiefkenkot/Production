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

BINANCE_API_KEY = pal.binance_key

def fetch_bybit_data(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {'category': 'spot'}
    response = requests.get(url, params=params)
    data = response.json()

    target_data = next((item for item in data['result']['list'] if item['symbol'] == symbol), None)

    if target_data is None:
        raise ValueError(f'Symbol {symbol} not found in the response data.')

    ask_price = float(target_data['ask1Price'])
    bid_price = float(target_data['bid1Price'])

    return ask_price, bid_price


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
    bid_price = float(target_data["bestBid"])

    return ask_price, bid_price

def fetch_and_append_data_merged(interval):

    bybit_pair = 'XRPUSDC'
    bybit_ask_price, bybit_bid_price = fetch_bybit_data(bybit_pair)

    bitget_pair = 'XRPUSDT_UMCBL'
    bitget_ask_price, bitget_bid_price = fetch_bitget_data(bitget_pair)

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        f'Bybit_{bybit_pair}_bid': [bybit_bid_price],
        f'Bybit_{bybit_pair}_ask': [bybit_ask_price],
        f'Bitget_{bitget_pair.replace("_", "")}_bid': [bitget_bid_price],
        f'Bitget_{bitget_pair.replace("_", "")}_ask': [bitget_ask_price]
    }

    df = pd.DataFrame(data_dict)

    csv_file = f"XRP_Bybit-Bitget - {interval} Sec.csv"

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

interval = 15

while True:
    try:
        merged_data_dict = fetch_and_append_data_merged(interval)
        time.sleep(interval)
    except Exception as e:
        print(f'Error: {e}')
        continue