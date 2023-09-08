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



symbol = 'BTCTUSD'

def fetch_binance_data(symbol):
    url = 'https://api.binance.com/api/v3/depth'
    headers = {'X-MBX-APIKEY': pal.binance_key}
    param = {'symbol': symbol}
    response = requests.get(url, headers=headers, params= param)
    data = response.json()

    pprint(data)

    # return ask_price, volume

# ask_price, volume = fetch_binance_data(symbol)
# fetch_binance_data(symbol)

# print(ask_price)
# print(volume)

# time.sleep(1234)


def bid_ask_ratio():
    url = 'https://api.binance.com/api/v3/depth'
    headers = {'X-MBX-APIKEY': pal.binance_key}
    param = {'symbol': symbol}
    response = requests.get(url, headers=headers, params= param)
    data = response.json()

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
    if not os.path.isfile(f'Binance_{symbol}_Orderbook.csv'):
        orderbook_df.to_csv(f'Binance_{symbol}_Orderbook.csv', mode='w', header=True, index=False)
    else:
        orderbook_df.to_csv(f'Binance_{symbol}_Orderbook.csv', mode='a', header=False, index=False)

df = pd.read_csv('Binance_BTCTUSD_Orderbook.csv')


def ratio(x, y, z):
    n=10
    ratio = df[f'ratio {n}']
    best_ask = df['best ask']
    best_bid = df['best bid']
    df['ma'] = best_ask.rolling(x).mean()
    df['sd'] = best_ask.rolling(x).std()
    df['z'] = (best_ask-df['ma']) / df['sd']
    df['+b'] = df['ma'] + (y * df['sd'])
    df['-b'] = df['ma'] - (y * df['sd'])

    # df['pos'] = np.where(best_ask > df['+b'], np.where(ratio > z, -1, 0), np.where(best_ask < df['-b'], np.where(ratio > z, 1, 0),0)) # reversion/LS
    df['pos'] = np.where(best_ask > df['+b'], np.where(ratio > z, 1, 0), np.where(best_ask < df['-b'], np.where(ratio > z, -1, 0),0)) # momentum/LS

    df['pos change'] = df['pos'].diff()
    df['entry'] = np.where(df['pos change'] != 0, best_ask, np.nan)
    df['entry'].fillna(method='ffill', inplace=True)
    # df['fee'] = best_ask * 0.00035*0
    df['fee'] = best_ask - best_bid
    # df['pnl'] = np.where((df['pos change'] != 0) & (df['pos change'].notnull()), best_bid - df['entry'].shift(1) - df['fee'], 0)
    df['pnl'] = np.where((df['pos change'] != 0) & (df['pos change'].notnull()), (df['entry'] - df['entry'].shift(1))* df['pos'].shift(1) - df['fee'], 0)
    df['cumu'] = df['pnl'].cumsum()
    df['trade_count'] = abs(df['pos change']).cumsum()

    # print(df.tail(2000))
    return pd.Series([x, y, z, df['cumu'].iloc[-1], df['trade_count'].iloc[-1]], index=['x','y', 'z', 'cumu', 'trade_count'])

#
while True:
    bid_ask_ratio()
    ratio()

    time.sleep(1)
