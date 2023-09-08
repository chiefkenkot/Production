import time
import numpy as np

import pandas as pd
import requests
import os
from datetime import datetime
import re
import pal
from CEX_Request_V2 import BinanceRequest
from CEX_Request_V2 import ByBitRequest


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


    if bybit_ask_price > binance_ask_price:
        if len(active_order['result']['list']) > 0: # check if have active order
            if active_order_side == 'Sell':
                print(f'Bybit has sell order')
            if active_order_side == 'Sell' and float(active_order_price) - bybit_ask_price > 10: # if price too far
                bybit_request.cancel_order('spot', bybit_symbol, order_id= active_orderid)
                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                         bybit_symbol, 'Limit',
                                                                         price=bybit_ask_price - slippage,
                                                                         qty=qty, is_leverage=0,
                                                                         order_filter='order',
                                                                         time_in_force='GTC')
                print(f'Bybit queue sell: {response}')

            elif active_order_side == 'Buy': # awaiting to settle pos
                bybit_request.cancel_order('spot', bybit_symbol, order_id=active_orderid)
                print(f'bybit_ask_price > binance_ask_price, active order = Buy, cancel order until valid again')
            else:
                print('bybit_ask_price > binance_ask_price, none of the situation has been met')


        elif bybit_BTC_balance < qty: # already have pos or q order, check Binance pos
            response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history(
                'spot')
            if transaction_status == 'Filled': # check if it is filled or not
                print(f'Bybit already short, balance = {bybit_BTC_balance}')
                if binance_BTC_balance < qty: # if have not bought at Binance
                    response, binance_transaction_price = binance_request.place_order(symbol='BTCTUSD', side='BUY',
                                                                              order_type='MARKET', quantity=qty)
                    transactions_data(binance_transaction=binance_transaction_price, bybit_transaction=bybit_transaction_price)
                    print(f'Binance Transaction: {response}')
            else: # if not filled, keep wait
                print(f'Waiting for next signal 1')

        elif bybit_BTC_balance >= qty: # no pos yet, open new pos
            bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
            response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                     bybit_symbol, 'Limit',
                                                                     price=bybit_ask_price - slippage,
                                                                     qty=qty, is_leverage=0,
                                                                     order_filter='order',
                                                                     time_in_force='GTC')
            print(f'Bybit queue sell: {response}')
        else:
            print('bybit_ask_price > binance_ask_price, nth happen')
            tg_pop('bybit_ask_price > binance_ask_price, nth happen')

        if order has been filled, buy binance


    if bybit_ask_price <= binance_ask_price:
        if len(active_order['result']['list']) > 0: # check if have active order
            print(f'bybit_ask_price <= binance_ask_price')
            if active_order_side == 'Buy':
                print(f'Bybit has buy order')
            if active_order_side == 'Buy' and bybit_bid_price - float(active_order_price) > 10: # if side invalid or if price too far
                bybit_request.cancel_order('spot', bybit_symbol, order_id= active_orderid)
                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                         bybit_symbol, 'Limit',
                                                                         price=bybit_bid_price + slippage,
                                                                         qty=qty, is_leverage=0,
                                                                         order_filter='order',
                                                                         time_in_force='GTC')
                print(f'Bybit queue buy: {response}')
            elif active_order_side == 'Sell': # if it is sell order, cancel until valid again
                bybit_request.cancel_order('spot', bybit_symbol, order_id=active_orderid)
                print(f'bybit_ask_price <= binance_ask_price, active order = Sell, cancel order until valid again')
            else:
                print('bybit_ask_price <= binance_ask_price, check if have active order')

        elif bybit_BTC_balance >= qty: # already have pos, check Binance pos
            response, bybit_transaction_price, transaction_status, transaction_side = bybit_request.get_order_history('spot')
            print(f'Bybit already long, balance = {bybit_BTC_balance}')
            if binance_BTC_balance >= qty:
                response, binance_transaction_price = binance_request.place_order(symbol='BTCTUSD', side='SELL',
                                                                          order_type='MARKET', quantity=qty)
                transactions_data(binance_transaction=binance_transaction_price, bybit_transaction=bybit_transaction_price)
                print(f'Binance Transaction: {response}')
            else:
                print(f'Waiting for next sell signal 2')

        elif bybit_BTC_balance < qty: # no pos yet, open new pos

            bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
            response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                     bybit_symbol, 'Limit',
                                                                     price=bybit_bid_price + slippage,
                                                                     qty=qty, is_leverage=0,
                                                                     order_filter='order',
                                                                     time_in_force='GTC')
            print(f'Bybit queue buy: {response}')
        else:
            print('bybit_ask_price <= binance_ask_price, nth happen')
            tg_pop('bybit_ask_price <= binance_ask_price, nth happen')



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



time.sleep(1234)
while True:
    try:

        # fetch_and_append_data_merged()
        base()
    except ConnectionError:
        continue
    except Exception as e:
        import traceback
        print(str(e))
        print(traceback.format_exc())
        tg_pop(str(e))
        break

