import pandas as pd
import numpy as np
from CEX_Request import ByBitRequest
from CEX_Request import BinanceRequest
from CEX_Request import Bitget_Request
import json
import uuid
import pal
import hmac
import hashlib
import urllib
import requests
from pprint import pprint
from datetime import datetime
import os
import time
import asyncio
import base64


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

bitget_api_key = pal.bitget_key
bitget_secret_key = pal.bitget_secret
bitget_pass_phrase = pal.bitget_pass_phrase
bitget_request = Bitget_Request(bitget_api_key, bitget_secret_key, bitget_pass_phrase)


binance_api_key = pal.binance_key
binance_api_secret = pal.binance_secret

###### Bitget Variable ######
bitget_symbol = 'BTCUSDT_UMCBL'
qty = 0.001

###### Binance Variable ######
binance_symbol = 'BTCTUSD'

###### Order Function ######
def rtq(bitget_symbol):
    url = "https://api.bitget.com/api/mix/v1/market/ticker"
    querystring = {"symbol": bitget_symbol}

    response = requests.get(url, params=querystring)
    data = response.json()

    if data["code"] == "00000" and "data" in data:
        target_data = data["data"]
    else:
        raise ValueError(f'Symbol {bitget_symbol} not found in the response data.')

    bitget_ask_price = float(target_data["bestAsk"])
    bitget_bid_price = float(target_data["bestBid"])

    return bitget_ask_price, bitget_bid_price

# bitget_ask_price, bitget_bid_price = rtq(symbol)

# while True:
#     bitget_ask_price, bitget_bid_price = rtq(symbol)
#     print(bitget_ask_price, bitget_bid_price)
#     time.sleep(1)

# orderid = bitget_request.place_single_order('BTCUSDT_UMCBL', 'sell_single', 0.001, 'limit', 31000)
#
# side, size, state = bitget_request.get_order_detail('BTCUSDT_UMCBL', order_id=orderid)

# Example
# bitget_ask_price, bitget_bid_price = rtq(bitget_symbol)
# bitget_request.place_single_order('BTCUSDT_UMCBL', 'sell_single', 0.001, 'limit', (bitget_ask_price+1000))
# bitget_request.place_single_order('BTCUSDT_UMCBL', 'buy_single', 0.001, 'limit', (bitget_bid_price-1000))
# bitget_request.place_single_order('BTCUSDT_UMCBL', 'buy_single', qty*2, 'limit', (bitget_bid_price-1000))
# bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
# time.sleep(1234)
# bitget_all_position, holding_symbol, holding_side, holding_size = bitget_request.get_all_positions('umcbl')
# # if bitget_all_position['data']:
# if holding_side not in ['long', 'short']:
#     print('holdng side == long')
# else:
#     print('no data')
#
# print(holding_symbol)
# print(holding_side)
# print(holding_size)
#
#
# time.sleep(1234)


# usdt_balance = bitget_request.get_account_list('umcbl')

# response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, 'USDT')
#
# print(holding_symbol)
# print(holding_side)
# print(type(holding_size))
#
#
#
# time.sleep(1234)


# ==================================================


def binance_market_buy(qty):
    api_key = binance_api_key
    secret_key = binance_api_secret

    binance_request = BinanceRequest(api_key, secret_key)

    response = binance_request.place_order(
        symbol='BTCTUSD',
        side='BUY',  # 'BUY' / 'SELL'
        order_type='MARKET',  # 'LIMIT' / 'MARKET'
        quantity=qty,  # BTC qty
    )
    print(response)


def binance_market_sell(qty):
    api_key = binance_api_key
    secret_key = binance_api_secret

    binance_request = BinanceRequest(api_key, secret_key)

    response = binance_request.place_order(
        symbol='BTCTUSD',
        side='SELL',  # 'BUY' / 'SELL'
        order_type='MARKET',  # 'LIMIT' / 'MARKET'
        quantity=qty,  # BTC qty
    )
    print(response)


def binance_position():
    api_key = binance_api_key
    secret_key = binance_api_secret
    binance_request = BinanceRequest(api_key, secret_key)
    account_info = binance_request.get_account_info()
    binance_balances = {
        balance['asset']: balance['free']
        for balance in account_info['balances']
        if float(balance['free']) > 0
    }
    # print(json.dumps(account_info, indent=2))
    # print(positive_balances)
    return binance_balances


# binance_balances = binance_position()

def fetch_binance_data(binance_symbol):
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    headers = {'X-MBX-APIKEY': pal.binance_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    target_data = None
    for item in data:
        if item['symbol'] == binance_symbol:
            target_data = item
            break

    if target_data is None:
        raise ValueError(f'Symbol {binance_symbol} not found in the response data.')

    binance_ask_price = float(target_data['askPrice'])
    binance_bid_price = float(target_data['bidPrice'])
    # volume = None  # The bookTicker endpoint does not provide 24-hour trading volume.

    return binance_ask_price, binance_bid_price


# binance_ask_price, binance_bid_price = fetch_binance_data(binance_symbol)

# print(binance_ask_price)
# print(binance_bid_price)
# time.sleep(1234)

def diff_rtq():
    # RTQ
    bitget_ask_price, bitget_bid_price = rtq(bitget_symbol)
    binance_ask_price, binance_bid_price = fetch_binance_data(binance_symbol)
    diff_now = round((binance_ask_price - float(bitget_ask_price)), 2)

    return diff_now

# while True:
#     diff_now = diff_rtq()
#     print(diff_now)
#     time.sleep(1)

###### Create CSV ######




def fetch_deribit_data(symbol):
    url = f'https://www.deribit.com/api/v2/public/get_order_book?instrument_name={symbol}&depth=1'
    response = requests.get(url)
    data = response.json()

    ask_price = float(data['result']['asks'][0][0])
    volume = float(data['result']['stats']['volume'])

    return ask_price, volume


def fetch_and_append_data_merged():
    binance_pair = 'BTCTUSD'
    binance_price, _ = fetch_binance_data(binance_pair)
    binance_header = 'Binance_' + binance_pair.replace('/', '')

    deribit_pair = 'BTC-PERPETUAL'
    deribit_price, _ = fetch_deribit_data(deribit_pair)
    deribit_header = 'Deribit_' + deribit_pair.replace('-', '')

    bitget_pair = 'BTCUSDT_UMCBL'
    bitget_price, _ = rtq(bitget_pair)  # Use the Bitget function here
    bitget_header = 'Bitget_' + bitget_pair.replace('-', '')

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        binance_header: [binance_price],
        deribit_header: [deribit_price],
        bitget_header: [bitget_price]  # Add the Bitget data here
    }

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_Deribit-Binance-Bitget.csv"  # Update the filename

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    # print(df)

    return data_dict


# orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty * 2, 'limit', 32000)
# while True:
#     try:
#         side, size, state = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
#         print(state)
#         print(size)
#         print(type(size)) # flaot
#         time.sleep(1)
#
#     except requests.exceptions.Timeout:
#         print("Request timed out. Retrying...")
#         continue
#
#     except Exception as e:
#         print(f'Error: {e}')
#         print('pos == 1, elif dead')
#         pass
#
# print('end')
# time.sleep(12345)
###### Order ######

# cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
# print(cancel_status)
# if cancel_status == 'No order to cancel':
#     print('yes')
# else:
#     print('no')
#
#
# time.sleep(1234)
def tg_pop(e):

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = (e)

    requests.get(base_url+message)



def base(x, y, cancel_counter, order_counter):
    start_time = time.time()
    print(f'start time = {start_time}')

    df = pd.read_csv('BTC_Deribit-Binance-Bitget.csv')
    df = df[['timestamp', 'Binance_BTCTUSD', 'Bitget_BTCUSDT_UMCBL', 'Deribit_BTCPERPETUAL']]
    df['diff'] = df['Binance_BTCTUSD'] - df['Bitget_BTCUSDT_UMCBL']
    df['ma'] = df['diff'].rolling(x).mean()
    df['sd'] = df['diff'].rolling(x).std()
    df['z'] = (df['diff'] - df['ma']) / df['sd']
    df['+b'] = df['ma'] + df['sd'] * y
    df['-b'] = df['ma'] - df['sd'] * y

    df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))
    pos = df['pos'].iloc[-1]
    diff1 = df['+b'].iloc[-1]
    diff2 = df['-b'].iloc[-1]
    # print(type(pos))
    # print(pos)

    print(df.tail(5))

    # fetch Bybit / Binance position
    binance_balances = binance_position()
    print(f'binance_balances: {binance_balances}')
    # bitget_all_position, holding_symbol, holding_side, holding_size = bitget_request.get_all_positions('umcbl')
    response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, 'USDT')
    # print(holding_symbol) #BTCUSDT_UMCBL
    # print(holding_side) #long/ short
    # print(holding_size) #0.001(qty)


    # demo
    # {'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '199.00000000', 'AXS': '0.00500000', 'WOO': '7.05479750'}
    # {'side': 'Sell', 'symbol': 'USDCUSDT', 'size': '10.0'} / {'side': 'None', 'symbol': 'USDCUSDT', 'size': '0.0'}

    # RTQ
    bitget_ask_price, bitget_bid_price = rtq(bitget_symbol)
    # binance_ask_price, binance_bid_price = fetch_binance_data(binance_symbol)
    # diff_now = binance_ask_price - float(bitget_ask_price)

    # print(f'bybit bid = {bybit_bid_price}, ask = {bybit_ask_price}')

    # fetch Bybit / Binance order
    # open_order = bybit_open_order(category, bybit_symbol)
    # print(f'get open order = {open_order}')
    # no open order, 0

    ###### place order ######
    if pos == 1:
        # if previously == 1, pass
        if holding_side == 'short' and holding_size > '0':
            print('signal = 1, position = 1')
            pass
        # if previously == -1
        elif holding_side == 'long' and holding_size > '0':
            orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty*2, 'limit', bitget_ask_price)
            counter = 0
            print('signal = 1, position = -1')
            print('long binance, short bitget')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff_now <= diff2:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            binance_market_buy(qty*2)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)

                    if counter == 3:
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        if state in ['new']:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        # need to check existing order size, unfilled order should have one more handling
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty*2)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty * 2)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == 1, elif dead')
                    pass

        # if there is no position, open new position
        else:
            orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, 'limit',bitget_ask_price)
            counter = 0
            print('signal = 1, position = 0')
            print('long binance, short bitget')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff_now <= diff2:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            binance_market_buy(qty)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)


                    if counter == 3:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == 1, else dead')
                    pass

    if pos == -1:
        # if previously == -1, pass
        if holding_side == 'long' and holding_size > '0':
            print('signal = -1, position = -1')
            pass
        # if previously == 1
        elif holding_side == 'short' and holding_size > '0':
            orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty*2, 'limit', bitget_bid_price)
            counter = 0
            print('signal = -1, position = 1')
            print('short binance,long bitget')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff_now >= diff1:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            binance_market_sell(qty*2)
                            order_counter += 1
                            print('Binance Market Sell')
                            break
                        time.sleep(1)

                    if counter == 3:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty*2)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty*2)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        time.sleep(1)
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == -1, elif dead')
                    pass

        # if there is no position, open new position
        else:
            orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, 'limit',bitget_bid_price)
            counter = 0
            print('signal = -1, position = 0')
            print('short binance,long bitget')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff_now >= diff1:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            binance_market_sell(qty)
                            order_counter += 1
                            print('Binance Market Sell')
                            break
                        time.sleep(1)


                    if counter == 3:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        time.sleep(1)
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == -1, elif dead')
                    pass

    if pos == 0:
        # if previously == -1
        if holding_side == 'long' and holding_size > '0':
            orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, 'limit', bitget_ask_price)
            counter = 0
            print('signal = 0, position = -1')
            print('long binance, short bitget')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff2 <= diff_now <= diff1:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            # print('bybit order filled')
                            binance_market_buy(qty)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)


                    if counter == 3:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_buy(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        time.sleep(1)
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == 1, elif dead')
                    pass

        # if previously == 1
        elif holding_side == 'short' and holding_size > '0':
            # bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price)
            orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, 'limit', bitget_bid_price)
            counter = 0
            print('signal = 0, position = 1')
            print('short binance,long bitget to settle all position')
            while counter < 3:
                try:
                    diff_now = diff_rtq()
                    counter += 1
                    print(f'counter = {counter}')
                    if diff2 <= diff_now <= diff1:
                        # Check if Bybit order is executed
                        state, size, side = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                        print(f'state = {state}')
                        if state in ['new', 'partially_filled']:
                            print(f'has open order:{orderid}')
                        else:
                            binance_market_sell(qty)
                            order_counter += 1
                            print('Binance Market Sell to settle all position')
                            break
                        time.sleep(1)

                    if counter == 3:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                    else:
                        cancel_status = bitget_request.cancel_all_orders(bitget_symbol, 'USDT')
                        print(f'bitget cancel status = {cancel_status}')
                        if cancel_status == 'No order to cancel':
                            binance_market_sell(qty)
                            order_counter += 1
                        else:
                            cancel_counter += 1
                        time.sleep(1)
                        break

                except requests.exceptions.Timeout:
                    print("Request timed out. Retrying...")
                    continue

                except Exception as e:
                    print(f'Error: {e}')
                    print('pos == 0, elif dead')
                    pass



        # if previously == 0
        else:
            print('signal = 0, position = 0')
            if holding_side not in ['long', 'short']:
                time.sleep(8)
                pass


    elapsed = time.time() - start_time
    print(f'elapsed = {elapsed}')
    if elapsed < 10:
        time.sleep(10 - elapsed)
    print('end')

    return order_counter, cancel_counter
    # time.sleep(1234)

###### Execution ######
counter = 0
cancel_counter = 0
order_counter = 0
while True:
    try:
        if counter < 51:
            merged_data_dict = fetch_and_append_data_merged()
            counter += 1
            print(f'accumulating data {counter}')
            time.sleep(10)

        else:
            merged_data_dict = fetch_and_append_data_merged()
            order_counter, cancel_counter = base(50, 0.4, cancel_counter, order_counter)
            print(f'order counter = {order_counter}')
            print(f'cancel counter = {cancel_counter}')

    except Exception as e:
        print(f'error: {e}')
        tg_pop(f'Bitget / Binance pair error: {e}')
        break

