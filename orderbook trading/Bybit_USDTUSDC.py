import datetime
import os.path
import time

import requests
import pal
from CEX_Request_V2 import Bitget_Request
from pprint import pprint
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# bitget_api_key = pal.hhyp_bitget_key_2
# bitget_secret_key = pal.hhyp_bitget_secret_2
# bitget_pass_phrase = pal.hhyp_bitget_pass_phrase_2
bitget_api_key = pal.bitget_key
bitget_secret_key = pal.bitget_secret
bitget_pass_phrase = pal.bitget_pass_phrase
bitget_request = Bitget_Request(bitget_api_key, bitget_secret_key, bitget_pass_phrase)

# url = "https://api.bitget.com/api/mix/v1/market/ticker"
# symbol = "BTCUSDT_UMCBL"
#
# querystring = {"symbol": symbol}
#
# response = requests.get(url, params=querystring)
#
# print(response.json())



symbol = 'USDCUSDT'


def fetch_bybit_data(symbol):
    url = 'https://api.bybit.com/v5/market/orderbook'
    params = {'category': 'spot',
              'symbol': symbol,
              'limit': 50}
    response = requests.get(url, params=params)
    data = response.json()

    ask = data['result']['a']
    bid = data['result']['b']


    # print(data)
    # print(ask)
    # print(bid)
    # volume = float(data['volume24h'])



# fetch_bybit_data(symbol=symbol)
#
#
# time.sleep(1234)

def trading_history(symbol):
    url = 'https://api.bybit.com/v5/market/recent-trade'
    param = {
        'category': 'spot',
        'symbol' : symbol
    }
    response = requests.get(url, params=param)
    response = response.json()
    data = response['result']['list']
    # pprint(response)

    total_volume = 0.0
    buy_volume = 0.0
    for i in data:
        size = float(i['size'])
        total_volume += abs(size)
        if i['side'] == 'Buy':
            buy_volume += size

    buy_ratio = (buy_volume / total_volume) * 100 if total_volume else 0
    print(f"Buy volume ratio: {buy_ratio}%")

    return buy_ratio


# trading_history(symbol)
# time.sleep(1234)

def bid_ask_ratio():
    url = 'https://api.bybit.com/v5/market/orderbook'
    params = {'category': 'spot',
              'symbol': symbol,
              'limit': 50}
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)

    best_ask = data['result']['a'][0][0]
    best_bid = data['result']['b'][0][0]
    # print(best_ask)
    # print(best_bid)

    asks_df = pd.DataFrame(data['result']['a'], columns=['Price', 'Quantity'])
    bids_df = pd.DataFrame(data['result']['b'], columns=['Price', 'Quantity'])

    asks_df['Quantity'] = pd.to_numeric(asks_df['Quantity'])
    bids_df['Quantity'] = pd.to_numeric(bids_df['Quantity'])

    depth = np.arange(1, 11, 1)
    timestamp = datetime.datetime.now()
    columns = ['timestamp', 'best bid', 'best ask']
    data_dict = {'timestamp': timestamp, 'best bid': [best_bid], 'best ask': [best_ask]}

    for i in depth:
        ask_cumsum = asks_df['Quantity'].head(i).sum()
        bid_cumsum = bids_df['Quantity'].head(i).sum()
        # print(ask_cumsum)
        # print(bid_cumsum)

        bid_ask_ratio = bid_cumsum / ask_cumsum
        columns.append(f'Depth {i}')
        data_dict[f'Depth {i}'] = [bid_ask_ratio]
        # print(f'depth = {i}: ratio = {bid_ask_ratio}')

    # Call the trading_history function to get the buy ratio
    buy_ratio = trading_history(symbol)

    # Add buy_ratio to the data dictionary
    columns.append('Buy Ratio')
    data_dict['Buy Ratio'] = [buy_ratio]

    orderbook_df = pd.DataFrame(data_dict, columns=columns)
    print(orderbook_df)
    if not os.path.isfile(f'Bybit_{symbol}_Orderbook.csv'):
        orderbook_df.to_csv(f'Bybit_{symbol}_Orderbook.csv', mode='w', header=True, index=False)
    else:
        orderbook_df.to_csv(f'Bybit_{symbol}_Orderbook.csv', mode='a', header=False, index=False)


# bid_ask_ratio()
#
# time.sleep(1234)

#
while True:
    bid_ask_ratio()
    time.sleep(1)
