import time
import numpy as np
import traceback
import pandas as pd
import requests
import os
from datetime import datetime
import re
import pal
from CEX_Request_V2 import BinanceRequest
from CEX_Request_V2 import ByBitRequest
import socket



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

bybit_api_key = pal.bybit_key
bybit_api_secret = pal.bybit_secret
bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)


binance_api_key = pal.binance_key
binance_api_secret = pal.binance_secret
binance_request = BinanceRequest(binance_api_key, binance_api_secret)




def fetch_and_append_data_merged():
    binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)
    binance_ask_header = 'Binance_' + binance_symbol.replace('/', '') + '_Ask'
    binance_bid_header = 'Binance_' + binance_symbol.replace('/', '') + '_Bid'

    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
    bybit_ask_header = 'Bybit_' + bybit_symbol + '_Ask'
    bybit_bid_header = 'Bybit_' + bybit_symbol + '_Bid'

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        binance_ask_header: [binance_ask_price],
        binance_bid_header: [binance_bid_price],
        bybit_ask_header: [bybit_ask_price],
        bybit_bid_header: [bybit_bid_price],
    }

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_Bybit-Binance_Data.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict


def transactions_data(binance_transaction, bybit_transaction):
    data = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Bybit': [bybit_transaction],
        'Binance': [binance_transaction],
        'fee': ['0']
    }
    df = pd.DataFrame(data)

    csv_file = f"Result_{ticker}-Bybit-Binance - {interval} Sec.csv"

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)


def tg_pop(message):

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    requests.get(base_url+message)


def base():

    # df = pd.read_csv('BTC_Bybit-Binance_Data.csv')
    # df = df[['timestamp','Binance_BTCTUSD_Ask', 'Binance_BTCTUSD_Bid', 'Bybit_BTCUSDC_Ask', 'Bybit_BTCUSDC_Bid']]
    #
    # df['ask_spread'] = df['Bybit_BTCUSDC_Ask'] - df['Binance_BTCTUSD_Ask']
    # df['bid_spread'] = df['Bybit_BTCUSDC_Bid'] - df['Binance_BTCTUSD_Bid']
    #
    # df['pos'] = 0
    # df.loc[df['ask_spread'] > 0, 'pos'] = -1
    # df.loc[df['ask_spread'] <= 0, 'pos'] = 1
    # pos = df['pos'].iloc[-1]
    #
    # print(df.tail(5))
    print('========================================')

    binance_balance = binance_request.get_account_info()
    binance_BTC_balance = float(binance_balance['BTC'])
    print(f'Binance position: {binance_balance}')
    bybit_balance = bybit_request.get_wallet_balance('spot')
    bybit_BTC_balance = bybit_balance['BTC']
    print(f'Bybit position: {bybit_balance}')


    # check spread
    binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)
    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
    ask_diff = bybit_ask_price - binance_ask_price
    active_order, active_order_side, active_order_price, active_order_status, active_orderid = bybit_request.get_open_orders('spot')
    data = {
        'timestamp': datetime.now(),
        'Bybit Bid': bybit_bid_price,
        'Bybit Ask': bybit_ask_price,
        'Binance Bid': binance_bid_price,
        'Binance Ask': binance_ask_price,
        'Diff': [bybit_ask_price - float(binance_ask_price)]
    }
    df = pd.DataFrame(data)
    print(df)


    if ask_diff > 0:
        if bybit_BTC_balance < qty: # already have pos, wait for signal change
            print(f'Already have Sell pos, waiting for signal change')
        elif bybit_BTC_balance >= qty: # no pos yet, open new pos
            bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
            response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                     bybit_symbol, 'Limit',
                                                                     price=bybit_ask_price - slippage,
                                                                     qty=qty, is_leverage=0,
                                                                     order_filter='order',
                                                                     time_in_force='GTC')
            print(f'Bybit Sell Order: {response}')
            while True:
                active_order, active_order_side, active_order_price, active_order_status, active_orderid = bybit_request.get_open_orders(
                    'spot')
                binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)
                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                ask_diff = bybit_ask_price - binance_ask_price
                if ask_diff > 0: # check if the signal is still valid or not
                    response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                        'spot')
                    try:

                        if float(active_order_price) - bybit_ask_price < 10: # if price still valid
                            if transaction_status == 'Filled':  # check if it is filled or not
                                response = binance_request.place_order(symbol='BTCTUSD',
                                                                       side='BUY',
                                                                       order_type='MARKET',
                                                                       quantity=qty)
                                print(f'Binance Transaction: {response}')
                                binance_transaction_price = response['fills'][0]['price']
                                transactions_data(binance_transaction=binance_transaction_price,
                                                  bybit_transaction=bybit_transaction_price)
                                print(f'Bybit already short, balance = {bybit_BTC_balance}')
                                print(f'Binance Transaction: {response}')
                                tg_pop(f'Transaction:\n'
                                       f'Short Bybit @ {bybit_transaction_price}\n'
                                       f'Long Binance @ {binance_transaction_price}\n'
                                       f'Spread = {bybit_transaction_price - binance_transaction_price}')
                            else:
                                print(f'transaction status: {active_order_status}')
                        else:
                            response, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=orderlink_id)
                            # time.sleep(0.3)
                            # history, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                            #     'spot')
                            # maybe need add biannce buy?
                            print(f'Cancel log: {response}')
                            print(f'Order Price > Ask Price $10')
                            break

                    except TypeError as e: # if it becomes taker and no active order
                        if str(e) == "float() argument must be a string or a number, not 'NoneType'":
                            response = binance_request.place_order(symbol='BTCTUSD',
                                                                   side='BUY',
                                                                   order_type='MARKET',
                                                                   quantity=qty)
                            print(f'Binance Transaction: {response}')
                            binance_transaction_price = response['fills'][0]['price']
                            transactions_data(binance_transaction=binance_transaction_price,
                                              bybit_transaction=bybit_transaction_price)
                            print(f'Bybit already short, balance = {bybit_BTC_balance}')
                            # print(f'Binance Transaction: {response}')
                            tg_pop(f'Transaction:\n'
                                   f'Short Bybit @ {bybit_transaction_price}\n'
                                   f'Long Binance @ {binance_transaction_price}\n'
                                   f'Spread = {bybit_transaction_price - binance_transaction_price}')

                else:
                    response, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=orderlink_id)
                    time.sleep(0.3)
                    history, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                        'spot')
                    if transaction_status == 'Filled': # if there is no order to cancel
                        response= binance_request.place_order(symbol='BTCTUSD',
                                                              side='BUY',
                                                              order_type='MARKET',
                                                              quantity=qty)
                        print(f'Binance Transaction: {response}')
                        binance_transaction_price = response['fills'][0]['price']
                        response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                            'spot')
                        transactions_data(binance_transaction=binance_transaction_price,
                                          bybit_transaction=bybit_transaction_price)
                        print(f'Bybit already short, balance = {bybit_BTC_balance}')
                        # print(f'Binance Transaction: {response}')
                        tg_pop(f'Transaction:\n'
                               f'Short Bybit @ {bybit_transaction_price}\n'
                               f'Long Binance @ {binance_transaction_price}\n'
                               f'Spread = {bybit_transaction_price - binance_transaction_price}')
                    else:
                        print(f'Cancel Success: {response}')
                        print(f'Bybit_ask_price < Binance_ask_price, ask_diff = {ask_diff}')
                    break

    elif ask_diff <= 0:
        if bybit_BTC_balance >= qty: # already have pos, wait for signal change
            print(f'Already have Buy pos, waiting for signal change')
        elif bybit_BTC_balance < qty: # no pos yet, open new pos
            bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
            response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                     bybit_symbol, 'Limit',
                                                                     price=bybit_bid_price + slippage,
                                                                     qty=qty, is_leverage=0,
                                                                     order_filter='order',
                                                                     time_in_force='GTC')
            print(f'Bybit Buy Order: {response}')
            while True:
                active_order, active_order_side, active_order_price, active_order_status, active_orderid = bybit_request.get_open_orders(
                    'spot')
                binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)
                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                ask_diff = bybit_ask_price - binance_ask_price
                if ask_diff <= 0: # check if the signal is still valid or not
                    response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                        'spot')
                    try:
                        if bybit_bid_price - float(active_order_price) < 10: # if price still valid
                            if transaction_status == 'Filled':  # check if it is filled or not
                                response = binance_request.place_order(symbol='BTCTUSD',
                                                                       side='SELL',
                                                                       order_type='MARKET',
                                                                       quantity=qty)
                                print(f'Binance Transaction: {response}')
                                binance_transaction_price = response['fills'][0]['price']
                                transactions_data(binance_transaction=binance_transaction_price,
                                                  bybit_transaction=bybit_transaction_price)
                                print(f'Bybit already long, balance = {bybit_BTC_balance}')
                                # print(f'Binance Transaction: {response}')
                                tg_pop(f'Transaction:\n'
                                       f'Long Bybit @ {bybit_transaction_price}\n'
                                       f'Short Binance @ {binance_transaction_price}\n'
                                       f'Spread = {binance_transaction_price - bybit_transaction_price}')
                            else:
                                print(f'transaction status: {active_order_status}')
                        else:
                            response, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=orderlink_id)
                            print(f'Cancel log: {response}')
                            print(f'Order Price < Bid Price $10')
                            break
                    except TypeError as e: # if it becomes taker and no active order
                        if str(e) == "float() argument must be a string or a number, not 'NoneType'":
                            response = binance_request.place_order(symbol='BTCTUSD',
                                                                   side='SELL',
                                                                   order_type='MARKET',
                                                                   quantity=qty)
                            print(f'Binance Transaction: {response}')
                            binance_transaction_price = response['fills'][0]['price']
                            transactions_data(binance_transaction=binance_transaction_price,
                                              bybit_transaction=bybit_transaction_price)
                            print(f'Bybit already long, balance = {bybit_BTC_balance}')
                            print(f'Binance Transaction: {response}')
                            tg_pop(f'Transaction:\n'
                                   f'Long Bybit @ {bybit_transaction_price}\n'
                                   f'Short Binance @ {binance_transaction_price}\n'
                                   f'Spread = {binance_transaction_price - bybit_transaction_price}')


                else:
                    response, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=orderlink_id)
                    time.sleep(0.3)
                    history, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                        'spot')
                    if transaction_status == 'Filled':# if there is no order to cancel
                        response = binance_request.place_order(symbol='BTCTUSD',
                                                               side='SELL',
                                                               order_type='MARKET',
                                                               quantity=qty)
                        print(f'Binance Transaction: {response}')
                        binance_transaction_price = response['fills'][0]['price']
                        response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                            'spot')
                        transactions_data(binance_transaction=binance_transaction_price,
                                          bybit_transaction=bybit_transaction_price)
                        print(f'Bybit already short, balance = {bybit_BTC_balance}')
                        # print(f'Binance Transaction: {response}')
                        tg_pop(f'Transaction:\n'
                               f'Short Bybit @ {bybit_transaction_price}\n'
                               f'Long Binance @ {binance_transaction_price}\n'
                               f'Spread = {bybit_transaction_price - binance_transaction_price}')
                    else:
                        print(f'Cancel Success: {response}')
                        print(f'Bybit_ask_price < Binance_ask_price, ask_diff = {ask_diff}')
                    break




###### Execution ######
ticker = 'BTC'
slippage = 0.5
interval = 0
qty = 0.001
binance_symbol = f'{ticker}TUSD'
bybit_symbol = f'{ticker}USDC'

# binance_balance = binance_request.get_account_info()
# binance_BTC_balance = binance_balance['BTC']
# print(f'Binance position: {binance_balance}')
# print(binance_BTC_balance)
# bybit_balance = bybit_request.get_wallet_balance('spot')
# bybit_BTC_balance = bybit_balance['BTC']
# print(f'Bybit position: {bybit_balance}')

# response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history('spot', orderLinkId=1693388371367778)
# print(response)
# response, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=1693388371367778)
# print(response)
# 1693388371367778
# 1693388374993856
# response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
#                                                          bybit_symbol, 'Limit',
#                                                          price=27000,
#                                                          qty=qty, is_leverage=0,
#                                                          order_filter='order',
#                                                          time_in_force='GTC')
#
# response2, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=orderlink_id)
# time.sleep(0.2)
# response3, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
#                         'spot')

# response2, retMsg = bybit_request.cancel_order('spot', bybit_symbol, order_link_id=1693479638714842)
# response2 = bybit_request.cancel_all_orders('spot', bybit_symbol)
# print(f'Cancel log: {response2}')
# print(f'History: {response3}')
# print(transaction_status)
# print(response)
#
# time.sleep(9999)

while True:
    try:
        # fetch_and_append_data_merged()
        base()
    except (ConnectionError, socket.error):
        continue
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        tg_pop(str(e))
        break



# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.16686230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 0.001000677, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 148.50316281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-30 14:22:40.864954   27324.07   27327.99     27345.74     27347.63 -19.64
# Already have Buy pos, waiting for signal change
# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.16686230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 0.001000677, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 148.50316281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask  Diff
# 0 2023-08-30 14:22:41.270902    27366.0   27369.18     27352.12     27361.21  7.97
# Bybit Sell Order: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498787234053231360', 'orderLinkId': '1693405361352329477'}, 'retExtInfo': {}, 'time': 1693405361363}
# Cancel Success: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498787234053231360', 'orderLinkId': '1693405361352329477'}, 'retExtInfo': {}, 'time': 1693405361636}
# Bybit_ask_price < Binance_ask_price, ask_diff = -12.260000000002037
# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.16686230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 6.77e-07, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 175.88228281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-30 14:22:42.088930   27378.96   27384.84     27396.46     27397.59 -12.75
# Bybit Buy Order: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498787240898294272', 'orderLinkId': '1693405362139803'}, 'retExtInfo': {}, 'time': 1693405362181}
# 'fills'
# Traceback (most recent call last):
#   File "C:\Users\Administrator\Desktop\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 338, in <module>
#     base()
#   File "C:\Users\Administrator\Desktop\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 243, in base
#     binance_transaction_price = response['fills'][0]['price']
# KeyError: 'fills'

# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.17877230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 0.001000677, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 148.50030281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask  Diff
# 0 2023-08-30 10:39:30.357786    27396.0    27403.6     27398.77     27399.87  3.73
# Bybit Sell Order: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498644711796145408', 'orderLinkId': '1693388371367778'}, 'retExtInfo': {}, 'time': 1693388371387}
# Cancel Success: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498644711796145408', 'orderLinkId': '1693388371367778'}, 'retExtInfo': {}, 'time': 1693388372766}
# Bybit_ask_price < Binance_ask_price, ask_diff = -18.450000000000728
# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.17877230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 6.77e-07, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 175.90169281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-30 10:39:34.339639   27398.03   27402.93     27421.32     27422.44 -19.51
# Bybit Buy Order: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1498644742129323264', 'orderLinkId': '1693388374993856'}, 'retExtInfo': {}, 'time': 1693388375003}
# 'fills'
# Traceback (most recent call last):
#   File "C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 317, in <module>
#     base()
#   File "C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 239, in base
#     quantity=qty)
#   File "C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Statistic Arbitrage\Binance VS Bybit\CEX_Request_V2.py", line 364, in place_order
#     transaction_price = response['fills'][0]['price']
# KeyError: 'fills'


# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.18452230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 0.001000677, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 148.46513281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-29 18:55:24.713871   27796.81   27801.95      27816.7     27818.82 -16.87
# Already have Buy pos, waiting for signal change
# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.18452230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 0.001000677, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 148.46513281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-29 18:55:26.213200    27840.0    27856.0     27818.81     27821.96  34.04
# Bybit_ask_price < Binance_ask_price, ask_diff = -16.970000000001164
# Already have Buy pos, waiting for signal change
# ========================================
# Binance position: {'BTC': '0.00010000', 'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '192.18452230', 'AXS': '0.00500000', 'WOO': '7.05479750'}
# Bybit position: {'AGI': 0.00964, 'AXL': 0.10398, 'BABYDOGE': 0.1215, 'BTC': 6.77e-07, 'CGPT': 0.11616, 'ETH': 0.01, 'MNT': 0.23229902, 'PLAY': 0.06059, 'RLTM': 0.00838, 'USDC': 176.40625281, 'USDT': 71.66321162574089}
#                    timestamp  Bybit Bid  Bybit Ask  Binance Bid  Binance Ask   Diff
# 0 2023-08-29 18:55:31.694939    27944.0   27949.96     27964.01     27968.83 -18.87
# float() argument must be a string or a number, not 'NoneType'
# Traceback (most recent call last):
#   File "C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 245, in <module>
#     base()
#   File "C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Statistic Arbitrage\Binance VS Bybit\Live V2.py", line 196, in base
#     if bybit_bid_price - float(active_order_price) < 10: # if price still valid
# TypeError: float() argument must be a string or a number, not 'NoneType'