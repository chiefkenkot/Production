import pandas as pd
import numpy as np
from CEX_Request import ByBitRequest
from CEX_Request import BinanceRequest
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


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

bybit_api_key = pal.bybit_key
bybit_secret_key = pal.bybit_secret
bybit_url = "https://api.bybit.com"
byrecv_window = str(5000)
bybit_request = ByBitRequest()
bybit_request.set_up(bybit_api_key, bybit_secret_key, byrecv_window, bybit_url)

binance_api_key = pal.binance_key
binance_api_secret = pal.binance_secret

###### Bybit Variable ######
bybit_symbol = 'BTCUSDT'
category = 'linear'
qty = '0.001'

###### Binance Variable ######
binance_symbol = 'BTCTUSD'


# category = 'linear'
# qty = '20'


###### Order Function ######
def bybit_rtq():
    response = bybit_request.get_market_price(category, bybit_symbol)
    response = response.json()
    bybit_ask_price = response['result']['a'][0][0]  # [a/b][price][size]
    bybit_ask_size = response['result']['a'][0][1]
    bybit_bid_price = response['result']['b'][0][0]
    bybit_bid_size = response['result']['b'][0][1]
    # pprint(response)

    return bybit_ask_price, bybit_bid_price


# bybit_ask_price, bybit_bid_price = rtq()
# print(bybit_ask_price, bybit_bid_price)


def bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price):
    orderlink_id = uuid.uuid4().hex

    bybit_request.place_limit_order(
        category=category,
        symbol=bybit_symbol,
        side='Sell',
        order_type="Limit",
        qty=qty,
        price=bybit_ask_price,
        time_in_force="GTC",
        order_link_id=orderlink_id,
        is_leverage=0,
        order_filter="Order"
    )

    return orderlink_id


# orderlink_id = bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price)


def bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price):
    orderlink_id = uuid.uuid4().hex

    bybit_request.place_limit_order(
        category=category,
        symbol=bybit_symbol,
        side='Buy',
        order_type="Limit",
        qty=qty,
        price=bybit_bid_price,
        time_in_force="GTC",
        order_link_id=orderlink_id,
        is_leverage=0,
        order_filter="Order"
    )

    return orderlink_id


# orderlink_id = bybit_future_limit_buy()


def bybit_open_order(category, bybit_symbol):
    try:
        open_order = bybit_request.get_open_orders(category=category, symbol=bybit_symbol)
        open_order = open_order.json()
        orderlink_id = open_order['result']['list'][0]['orderLinkId']
        # pprint(open_order)
        # print(orderlink_id)
        return orderlink_id

    except:
        # print('no queue order')
        return 0


# open_order = bybit_open_order(category, bybit_symbol)
# # if open_order != 0:
# #     print('has order')
# #     print(open_order)
# #
# # else:
# #     print('no order')
#
# print(open_order)
# time.sleep(1234)

def bybit_position(category, bybit_symbol):
    position = bybit_request.get_position_info(category=category, symbol=bybit_symbol)
    position = position.json()
    result = position['result']['list']

    side = result[0]['side']
    symbol = result[0]['symbol']
    size = result[0]['size']

    # Creating a new dictionary
    bybit_balance = {
        'side': side,
        'symbol': symbol,
        'size': size
    }

    return bybit_balance, side, symbol, size


# bybit_balance = bybit_position(category, bybit_symbol)
# if 'BTCUSDT' in positive_positions:
#     print('yes')
#
# else:
#     print('no')

# print(positive_positions)

# Response JSON: {'retCode': 0, 'retMsg': 'OK', 'result': {'list': [{'positionIdx': 0, 'riskId': 1, 'riskLimitValue': '200000', 'symbol': 'USDCUSDT', 'side': 'Sell', 'size': '10.0', 'avgPrice': '1.0003', 'positionValue': '10.003', 'tradeMode': 0, 'positionStatus': 'Normal', 'autoAddMargin': 0, 'adlRankIndicator': 2, 'leverage': '10', 'positionBalance': '1.00790198', 'markPrice': '1.0004', 'liqPrice': '28.1725', 'bustPrice': '28.1825', 'positionMM': '2.81825', 'positionIM': '0.20006', 'tpslMode': 'Full', 'takeProfit': '0.0000', 'stopLoss': '0.0000', 'trailingStop': '0.0000', 'unrealisedPnl': '-0.001', 'cumRealisedPnl': '-0.00665177', 'createdTime': '1675911855603', 'updatedTime': '1688847082107'}], 'nextPageCursor': '', 'category': 'linear'}, 'retExtInfo': {}, 'time': 1688847182005}


# time.sleep(5)
def cancel_order(category, bybit_symbol, orderlink_id):
    bybit_request.cancel_order(category=category, symbol=bybit_symbol, order_link_id=orderlink_id)


def cancel_all(category, bybit_symbol):
    bybit_request.cancel_all_orders(category=category, symbol=bybit_symbol)


# cancel_all(category, bybit_symbol)
# cancel_order()

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
    bybit_ask_price, bybit_bid_price = bybit_rtq()
    binance_ask_price, binance_bid_price = fetch_binance_data(binance_symbol)
    diff_now = binance_ask_price - float(bybit_ask_price)

    return diff_now


###### Create CSV ######


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

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        binance_header: [binance_price],
        bybit_header: [bybit_price],
        deribit_header: [deribit_price]
    }

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_Deribit-Bybit-Binance.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    # print(df)

    return data_dict


###### Order ######

# print('done')
# time.sleep(1234)


def base(x, y, cancel_counter, order_counter):
    start_time = time.time()
    print(f'start time = {start_time}')

    df = pd.read_csv('BTC_Deribit-Bybit-Binance.csv')
    df = df[['timestamp', 'Binance_BTCTUSD', 'Bybit_BTCUSDT', 'Deribit_BTCPERPETUAL']]
    df['diff'] = df['Binance_BTCTUSD'] - df['Bybit_BTCUSDT']
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
    print(binance_balances)
    bybit_balance, side, symbol, size = bybit_position(category, bybit_symbol)
    print(bybit_balance)

    # demo
    # {'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '199.00000000', 'AXS': '0.00500000', 'WOO': '7.05479750'}
    # {'side': 'Sell', 'symbol': 'USDCUSDT', 'size': '10.0'} / {'side': 'None', 'symbol': 'USDCUSDT', 'size': '0.0'}

    # RTQ
    bybit_ask_price, bybit_bid_price = bybit_rtq()
    binance_ask_price, binance_bid_price = fetch_binance_data(binance_symbol)
    # diff_now = binance_ask_price - float(bybit_ask_price)

    # print(f'bybit bid = {bybit_bid_price}, ask = {bybit_ask_price}')

    # fetch Bybit / Binance order
    # open_order = bybit_open_order(category, bybit_symbol)
    # print(f'get open order = {open_order}')
    # no open order, 0

    ###### place order ######
    if pos == 1:
        # if previously == 1, pass
        if side == 'Sell' and size > '0':
            print('1, 1')
            # time.sleep(8)
            pass
        # if previously == -1
        elif side == 'Buy' and size > '0':
            print('1, -1')
            bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price)
            bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price)
            counter = 0
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now < diff2:
                        print('long binance, short bybit')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            # print('bybit order filled')
                            binance_market_buy(qty)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)
                        counter += 1

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')


                except:
                    print('pos == 1, elif dead')
                    pass

        # if there is no position, open new position
        else:
            bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price)
            counter = 0
            print('1, 0')
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now < diff2:
                        print('long binance, short bybit')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            binance_market_buy(qty)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)
                        counter += 1

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')

                except:
                    print('pos == 1, else dead')
                    pass

    if pos == -1:
        # if previously == -1, pass
        if side == 'Buy' and size > '0':
            print('-1, -1')
            pass
        # if previously == 1
        elif side == 'Sell' and size > '0':
            print('-1, 1')
            bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price)
            bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price)
            counter = 0
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now > diff1:
                        print('short binance,long bybit')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            binance_market_sell(qty)
                            order_counter += 1
                            print('Binance Market Sell')
                            break

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')

                except:
                    print('pos == -1, elif dead')
                    pass

        # if there is no position, open new position
        else:
            bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price)
            print('-1, 0')
            counter = 0
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now > diff1:
                        print('short binance,long bybit')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            binance_market_sell(qty)
                            order_counter += 1
                            print('Binance Market Sell')
                            break
                        time.sleep(1)
                        counter += 1

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')

                except:
                    print('pos == -1, elif dead')
                    pass

    if pos == 0:
        # if previously == -1
        if side == 'Buy' and size > '0':
            bybit_future_limit_sell(category, bybit_symbol, bybit_ask_price)
            counter = 0
            print('0, -1')
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now < diff2:
                        print('long binance, short bybit')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            # print('bybit order filled')
                            binance_market_buy(qty)
                            order_counter += 1
                            print('Binance Market Buy')
                            break
                        time.sleep(1)
                        counter += 1

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')

                except:
                    print('pos == 1, elif dead')
                    pass

        # if previously == 1
        elif side == 'Sell' and size > '0':
            bybit_future_limit_buy(category, bybit_symbol, bybit_bid_price)
            counter = 0
            print('0, 1')
            while counter < 8:
                try:
                    diff_now = diff_rtq()

                    if diff_now > diff1:
                        print('short binance,long bybit to settle all position')
                        # Check if Bybit order is executed
                        open_order = bybit_open_order(category, bybit_symbol)
                        if open_order != 0:
                            print(f'has open order:{open_order}')
                        else:
                            binance_market_sell(qty)
                            order_counter += 1
                            print('Binance Market Sell to settle all position')
                            break
                        time.sleep(1)
                        counter += 1

                    if counter == 8:
                        cancel_all(category, bybit_symbol)
                        cancel_counter += 1
                        print('order cancelled')

                except:
                    print('pos == 0, elif dead')
                    pass

        # if previously == 0
        else:
            print('0, 0')
            if side == 'None' and size == '0.0':
                time.sleep(8)
                pass


    elapsed = time.time() - start_time
    print(f'elapsed = {elapsed}')
    if elapsed < 10:
        time.sleep(10 - elapsed)
    print('end')
    # time.sleep(1234)


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
            base(50, 0.4, cancel_counter, order_counter)
    except:
        print('error')
        break




# start_time = time.time()
#
#
# while True:
#     # print(start_time)
#
#     elapsed = time.time() - start_time
#     if elapsed < 10:
#         time.sleep(10 - elapsed)
#         print(f'elapsed = {elapsed}')
#
#     else:
#         print(f'start = {start_time}')
#
#     start_time = time.time()


