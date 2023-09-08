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

ask_price, volume = fetch_binance_data(symbol)

# print(ask_price)
# print(volume)

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
    ask_size = float(target_data["askSz"])
    bid_size = float(target_data["bidSz"])
    print(data)

    return ask_price, bid_price, ask_size, bid_size

bitget_symbol = 'BTCUSDT_UMCBL'

fetch_bitget_data(bitget_symbol)


# def bid_ask_ratio():
#     response = bitget_request.get_depth(bitget_symbol)
#     data = response['data']
#
#     asks_df = pd.DataFrame(data['asks'], columns=['Price', 'Quantity'])
#     asks_df['Type'] = 'Ask'
#     bids_df = pd.DataFrame(data['bids'], columns=['Price', 'Quantity'])
#     bids_df['Type'] = 'Bid'
#
#     asks_df['Quantity'] = pd.to_numeric(asks_df['Quantity'])
#     bids_df['Quantity'] = pd.to_numeric(bids_df['Quantity'])
#
#     ask_cumsum = asks_df['Quantity'].head(depth).cumsum()
#     bid_cumsum = bids_df['Quantity'].head(depth).cumsum()
#
#     print(ask_cumsum)
#     print(bid_cumsum)
#
#     bid_ask_ratio = bid_cumsum / ask_cumsum
#
#     print(bid_ask_ratio)
#
#
#     order_book_df = pd.concat([asks_df.head(depth), bids_df.head(depth)])
#     print(order_book_df)
#     order_book_df.to_csv('order_book.csv', index=False)


def bid_ask_ratio():
    response = bitget_request.get_depth(bitget_symbol)
    data = response['data']

    best_ask = data['asks'][0][0]
    best_bid = data['bids'][0][0]
    # print(best_ask)
    # print(best_bid)

    asks_df = pd.DataFrame(data['asks'], columns=['Price', 'Quantity'])
    bids_df = pd.DataFrame(data['bids'], columns=['Price', 'Quantity'])

    asks_df['Quantity'] = pd.to_numeric(asks_df['Quantity'])
    bids_df['Quantity'] = pd.to_numeric(bids_df['Quantity'])

    depth = np.arange(5, 55, 5)
    timestamp = datetime.datetime.now()
    columns = ['timestamp', 'best bid', 'best ask']
    data_dict = {'timestamp': timestamp, 'best bid': [best_bid], 'best ask': [best_ask]}

    for i in depth:
        ask_cumsum = asks_df['Quantity'].head(i).sum()
        bid_cumsum = bids_df['Quantity'].head(i).sum()
        # print(ask_cumsum)
        # print(bid_cumsum)

        bid_ask_ratio = bid_cumsum / ask_cumsum
        columns.append(f'ratio {i}')
        data_dict[f'ratio {i}'] = [bid_ask_ratio]
        # print(f'depth = {i}: ratio = {bid_ask_ratio}')

    orderbook_df = pd.DataFrame(data_dict, columns=columns)
    print(orderbook_df)
    if not os.path.isfile('Bitget_BTC_Orderbook.csv'):
        orderbook_df.to_csv('Bitget_BTC_Orderbook.csv', mode='w', header=True, index=False)
    else:
        orderbook_df.to_csv('Bitget_BTC_Orderbook.csv', mode='a', header=False, index=False)


# bid_ask_ratio()
#
# time.sleep(1234)


while True:
    bid_ask_ratio()
    time.sleep(1)
