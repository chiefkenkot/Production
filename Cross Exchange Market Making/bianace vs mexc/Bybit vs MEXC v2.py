import socket
import time
import json
import pandas as pd
import requests
import os
from datetime import datetime
import ccxt
import pal
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Replace these with your actual Binance and MEXC API keys
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
    # ask_volume = float(data['askQty'])
    return ask_price, bid_price

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
        'Diff': [bybit_ask_price - mexc_ask]
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


def tg_pop(message):

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    requests.get(base_url+message)


def logic():
    df = pd.read_csv('BTC_Bybit-MEXC_Data.csv')
    df = df[['timestamp', 'MEXC_BTC/USDT_Ask', 'MEXC_BTC/USDT_Bid', 'Bybit_BTCUSDC_Ask', 'Bybit_BTCUSDC_Bid']]

    df['ask_diff'] = df['Bybit_BTCUSDC_Ask'] - df['MEXC_BTC/USDT_Ask']
    # df['bid_diff'] = df['Bybit_BTCUSDC_Bid'] - df['MEXC_BTC/USDT_Bid']

    df['pos'] = np.nan
    df.loc[df['ask_diff'] > 5, 'pos'] = -1
    df.loc[df['ask_diff'] <= -5, 'pos'] = 1
    df['pos'] = df['pos'].ffill()


    df['pos_change'] = df['pos'].diff()
    pos = df['pos'].iloc[-1]
    spread = df['Bybit_BTCUSDC_Ask'].iloc[-1] - df['MEXC_BTC/USDT_Ask'].iloc[-1]
    if pd.isna(df['pos_change'].iloc[-1]):
        pass
    elif df['pos_change'].iloc[-1] != df['pos_change'].shift(1).iloc[-1]:
        print(f'pos changed: {pos}, spread = {spread}')
        tg_pop(f'pos changed: {pos}, spread = {spread}')

    # df['sum'] = abs(df['pos_change']).cumsum() / 2

    # print(df.head(2000))
    # print(df)

data_row = 0

while True:
    try:
        fetch_and_append_data()
        data_row += 1
        if data_row >2:
            logic()
        time.sleep(1)
    except (ConnectionError, socket.error):
        continue

# while True:
#     try:
#         fetch_and_append_data()
#         time.sleep(1)
#     except (ConnectionError, socket.error):
#         continue
