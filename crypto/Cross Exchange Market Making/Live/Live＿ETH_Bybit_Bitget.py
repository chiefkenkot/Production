import pandas as pd
import numpy as np
from CEX_Request_V2 import BinanceRequest
from CEX_Request_V2 import Bitget_Request
from CEX_Request_V2 import ByBitRequest
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

bitget_api_key = pal.hhyp_bitget_key_2
bitget_secret_key = pal.hhyp_bitget_secret_2
bitget_pass_phrase = pal.hhyp_bitget_pass_phrase_2
bitget_request = Bitget_Request(bitget_api_key, bitget_secret_key, bitget_pass_phrase)

# bybit_api_key = pal.bybit_key
# bybit_api_secret = pal.bybit_secret
# bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)

bybit_api_key = pal.hhyp_bybit_key_1
bybit_api_secret = pal.hhyp_bybit_secret_1
bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)


binance_api_key = pal.binance_key
binance_api_secret = pal.binance_secret



###### Order Function ######

# while True:
#     bitget_ask, bitget_bid = bitget_request.fetch_bitget_data(bitget_symbol)
#     print(bitget_ask)
#     print(bitget_bid)
#
#     bybit_ask, bybit_bid =bybit_request.fetch_bybit_data(bybit_symbol)
#     print(bybit_ask)
#     print(bybit_bid)
#
#     time.sleep(5)
#
# time.sleep(1234)

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



def diff_rtq():
    # RTQ
    bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)
    bybit_ask_price, bybit_bid_price =bybit_request.fetch_bybit_data(bybit_symbol)
    diff_now = round((bybit_ask_price - float(bitget_ask_price)), 2)

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
    bid_price = float(data['result']['bids'][0][0])


    return ask_price, bid_price


def fetch_and_append_data_merged(interval):

    bybit_pair = bybit_symbol
    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)

    deribit_pair = 'ETH-PERPETUAL'
    deribit_ask_price, deribit_bid_price = fetch_deribit_data(deribit_pair)

    bitget_pair = bitget_symbol
    bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        f'Bybit_{bybit_pair}_bid': [bybit_bid_price],
        f'Bybit_{bybit_pair}_ask': [bybit_ask_price],
        f'Deribit_{deribit_pair.replace("-", "")}_bid': [deribit_bid_price],
        f'Deribit_{deribit_pair.replace("-", "")}_ask': [deribit_ask_price],
        f'Bitget_{bitget_pair.replace("_", "")}_bid': [bitget_bid_price],
        f'Bitget_{bitget_pair.replace("_", "")}_ask': [bitget_ask_price]
    }

    df = pd.DataFrame(data_dict)

    csv_file = f"ETH_Deribit-Bybit-Bitget - {interval} Sec.csv"

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

# bybit_request.place_market_order('spot', 'Buy', bybit_symbol, 'Market', qty*2, is_leverage=0, order_filter='order')
# bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
# bybit_balance, side, symbol, size = bybit_request.get_position_info(category, bybit_symbol)
# bybit_balance= bybit_request.get_wallet_balance('spot')
# print(bybit_balance)


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





def base(x, y, cancel_counter, order_counter, interval):
    start_time = time.time()
    print(f'start time = {start_time}')

    df = pd.read_csv(f'ETH_Deribit-Bybit-Bitget - {interval} Sec.csv')
    df = df[
        ['timestamp', 'Bybit_ETHUSDC_bid', 'Bybit_ETHUSDC_ask', 'Bitget_ETHUSDTUMCBL_bid', 'Bitget_ETHUSDTUMCBL_ask']]
    df['diff'] = df['Bybit_ETHUSDC_ask'] - df['Bitget_ETHUSDTUMCBL_ask']
    df['ma'] = df['diff'].rolling(x).mean()
    df['sd'] = df['diff'].rolling(x).std()
    df['z'] = (df['diff'] - df['ma']) / df['sd']
    df['+b'] = df['ma'] + df['sd'] * y
    df['-b'] = df['ma'] - df['sd'] * y

    df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))
    pos = df['pos'].iloc[-1]
    diff1 = float(df['+b'].iloc[-1])
    diff2 = float(df['-b'].iloc[-1])
    # print(type(pos)) #<class 'numpy.int32'>
    # print(pos)

    print(df.tail(5))

    # fetch Bybit / Binance position
    bybit_balance = bybit_request.get_wallet_balance('spot')
    print(f'Bybit position: {bybit_balance}')
    # bitget_all_position, holding_symbol, holding_side, holding_size = bitget_request.get_all_positions('umcbl')
    response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, marginCoin)
    print(f'Bitget position: {response}')
    # print(holding_symbol) #BTCUSDT_UMCBL
    # print(holding_side) #long/ short
    # print(holding_size) #0.001(qty)

    # demo
    # {'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '199.00000000', 'AXS': '0.00500000', 'WOO': '7.05479750'}
    # {'side': 'Sell', 'symbol': 'USDCUSDT', 'size': '10.0'} / {'side': 'None', 'symbol': 'USDCUSDT', 'size': '0.0'}

    # RTQ
    bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)
    # bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
    # diff_now = binance_ask_price - float(bitget_ask_price)

    # print(f'bybit bid = {bybit_bid_price}, ask = {bybit_ask_price}')

    # pos = 1

    ###### place order ######
    try:
        if pos == 1:

            # if previously == 1, pass
            if holding_side == 'short' and holding_size > '0':
                print('signal = 1, position = 1')
                pass
            # if previously == -1
            elif holding_side == 'long' and holding_size > '0':
                orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty*2, marginCoin, 'limit', bitget_ask_price)
                counter = 0
                print('signal = 1, position = -1')
                print('long bybit, short bitget')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now <= diff2:
                            print(f'diff_now = {diff_now}, diff2 = {diff2}')
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty*2, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                                print('bybit Market Buy')
                                break
                            time.sleep(1)

                        elif diff_now > diff2:
                            print(f'diff_now = {diff_now}, diff2 = {diff2}')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty * 2, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            break

                        if counter == 3:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty * 2, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1


                    except requests.exceptions.Timeout:
                        print("Request timed out. Retrying...")
                        continue

                    except Exception as e:
                        print(f'Error: {e}')
                        print('pos == 1, elif dead')
                        pass

        # if there is no position, open new position
            else:
                orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, marginCoin, 'limit',bitget_ask_price)
                counter = 0
                print('signal = 1, position = 0')
                print('long bybit, short bitget')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now <= diff2:
                            print(f'diff_now = {diff_now}, type = {type(diff_now)} diff2 = {diff2}, type = {type(diff2)}')
                            print(diff_now <= diff2)
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                                print('bybit Market Buy')
                                break
                            time.sleep(1)

                        elif diff_now > diff2:
                            print(f'diff_now = {diff_now}, type = {type(diff_now)} diff2 = {diff2}, type = {type(diff2)}')
                            print(diff_now <= diff2)
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            break

                        if counter == 3:
                            print('counter == 3')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1


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
                orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty*2, marginCoin, 'limit', bitget_bid_price)

                counter = 0
                print('signal = -1, position = 1')
                print('short bybit,long bitget')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now >= diff1:
                            print(f'diff_now = {diff_now}, diff1 = {diff1}')
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty*2, is_leverage=0, order_filter='order')
                                order_counter += 1
                                print('bybit Market Sell')
                                break
                            time.sleep(1)

                        elif diff_now < diff1:
                            print(f'diff_now = {diff_now}, diff1 = {diff1}')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty*2, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            time.sleep(1)
                            break

                        if counter == 3:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty*2, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1


                    except requests.exceptions.Timeout:
                        print("Request timed out. Retrying...")
                        continue

                    except Exception as e:
                        print(f'Error: {e}')
                        print('pos == -1, elif dead')
                        pass

            # if there is no position, open new position
            else:
                orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, marginCoin, 'limit',bitget_bid_price)
                counter = 0
                print('signal = -1, position = 0')
                print('short bybit,long bitget')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now >= diff1:
                            print(f'diff_now = {diff_now}, diff1 = {diff1}')
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                                print('bybit Market Sell')
                                break
                            time.sleep(1)

                        elif diff_now < diff1:
                            print(f'diff_now = {diff_now}, diff1 = {diff1}')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            time.sleep(1)
                            break


                        if counter == 3:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1


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
                orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, marginCoin, 'limit', bitget_ask_price)
                counter = 0
                print('signal = 0, position = -1')
                print('long bybit, short bitget')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff2 <= diff_now <= diff1:
                            print(f'diff2 = {diff2}, diff_now = {diff_now}, diff1 = {diff1}')
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                                print('bybit Market Buy')
                                break
                            time.sleep(1)

                        elif diff2 > diff_now or diff_now > diff1:
                            print(f'diff2 = {diff2}, diff_now = {diff_now}, diff1 = {diff1}')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            time.sleep(1)
                            break


                        if counter == 3:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                bybit_request.place_limit_order('spot', 'Buy', bybit_symbol, 'Limit',
                                                                price=bybit_ask_price + 2, qty=qty, is_leverage=0,
                                                                order_filter='order', time_in_force='GTC')
                                order_counter += 1
                            else:
                                cancel_counter += 1


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
                orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, marginCoin, 'limit', bitget_bid_price)

                counter = 0
                print('signal = 0, position = 1')
                print('short bybit,long bitget to settle all position')
                while counter < 3:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff2 <= diff_now <= diff1:
                            print(f'diff2 = {diff2}, diff_now = {diff_now}, diff1 = {diff1}')
                            # Check if Bybit order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                                print('bybit Market Sell to settle all position')
                                break
                            time.sleep(1)

                        elif diff2 > diff_now or diff_now > diff1:
                            print(f'diff2 = {diff2}, diff_now = {diff_now}, diff1 = {diff1}')
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1
                            time.sleep(1)
                            break

                        if counter == 3:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                bybit_request.place_market_order('spot', 'Sell', bybit_symbol, 'Market', qty, is_leverage=0, order_filter='order')
                                order_counter += 1
                            else:
                                cancel_counter += 1


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

    except Exception as e:
        if "'NoneType' object is not subscriptable" in str(e):
            tg_pop(f'Bitget / Bybit ETH error: {e},\n\n , code restarting')
            pass


    elapsed = time.time() - start_time
    print(f'elapsed = {elapsed}')
    if elapsed < 10:
        time.sleep(10 - elapsed)
    print('end')

    return order_counter, cancel_counter
    # time.sleep(1234)


###### Bitget Variable ######
bitget_symbol = 'ETHUSDT_UMCBL'
qty = 0.05
product_type = 'UMCBL'
marginCoin = 'USDT'
response = bitget_request.set_position_mode(product_type, 'single_hold')
print(response)

###### Bybit Variable ######
bybit_symbol = 'ETHUSDC'
# bybit_symbol = 'USDCUSDT'
category = 'spot'

###### Execution ######
counter = 0
cancel_counter = 0
order_counter = 0
interval = 10


while True:
    try:
        if counter < 51:
            merged_data_dict = fetch_and_append_data_merged(interval=interval)
            counter += 1
            print(f'accumulating data {counter}')
            time.sleep(interval)

        else:
            merged_data_dict = fetch_and_append_data_merged(interval=interval)
            order_counter, cancel_counter = base(50, 0.4, cancel_counter, order_counter, interval)
            print(f'order counter = {order_counter}')
            print(f'cancel counter = {cancel_counter}')

    except Exception as e:
        print(f'error: {e}')
        import traceback
        print(traceback.format_exc())
        tg_pop(f'Bitget / Bybit ETH error: {e},\n traceback: {traceback.format_exc()}')
        break

