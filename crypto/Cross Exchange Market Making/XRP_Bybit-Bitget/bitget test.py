import time

import requests
import pal
from CEX_Request_V2 import Bitget_Request
from pprint import pprint
import pandas as pd

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

def bid_ask_ratio():
    response = bitget_request.get_depth(bitget_symbol)
    # pprint(response)

    # Assuming "response" is your data
    data = response['data']

    # Create a DataFrame for asks and bids
    asks_df = pd.DataFrame(data['asks'], columns=['Price', 'Quantity'])
    asks_df['Type'] = 'Ask'
    bids_df = pd.DataFrame(data['bids'], columns=['Price', 'Quantity'])
    bids_df['Type'] = 'Bid'

    # Convert the 'Quantity' column to numeric
    asks_df['Quantity'] = pd.to_numeric(asks_df['Quantity'])
    bids_df['Quantity'] = pd.to_numeric(bids_df['Quantity'])

    # Calculate the cumulative sum of the first 5 ask and bid volumes
    ask_cumsum = asks_df['Quantity'].head(5).cumsum()
    bid_cumsum = bids_df['Quantity'].head(5).cumsum()

    # Calculate the bid ask ratio
    bid_ask_ratio = bid_cumsum / ask_cumsum

    # Add the 'Bid_Ask_Ratio' column to the dataframe
    asks_df['Bid_Ask_Ratio'] = bid_ask_ratio.values  # add the ratio to the 'asks' dataframe

    # Concatenate the asks and bids DataFrames
    order_book_df = pd.concat([asks_df.head(5), bids_df.head(5)])

    # Save to CSV file
    order_book_df.to_csv('order_book.csv', index=False)

depth = 5

while True:
    bid_ask_ratio()
