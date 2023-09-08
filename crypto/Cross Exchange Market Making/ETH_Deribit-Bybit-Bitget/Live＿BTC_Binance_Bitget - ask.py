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

bitget_api_key = pal.hhyp_bitget_key_1
bitget_secret_key = pal.hhyp_bitget_secret_1
bitget_pass_phrase = pal.hhyp_bitget_pass_phrase_1
# bitget_api_key = pal.bitget_key
# bitget_secret_key = pal.bitget_secret
# bitget_pass_phrase = pal.bitget_pass_phrase
bitget_request = Bitget_Request(bitget_api_key, bitget_secret_key, bitget_pass_phrase)

bybit_api_key = pal.bybit_key
bybit_api_secret = pal.bybit_secret
bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)


binance_api_key = pal.hhyp_binance_key_1
binance_api_secret = pal.hhyp_binance_secret_1
binance_request = BinanceRequest(binance_api_key, binance_api_secret)



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

#

# print(response)




def diff_rtq():
    # RTQ
    bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)
    binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)
    diff_now = round((float(bitget_ask_price) - binance_ask_price), 2)

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

    binance_pair = binance_symbol
    binance_ask_price, binance_bid_price = binance_request.fetch_binance_data(binance_symbol)

    deribit_pair = 'BTC-PERPETUAL'
    deribit_ask_price, deribit_bid_price = fetch_deribit_data(deribit_pair)

    bitget_pair = bitget_symbol
    bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)

    data_dict = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        f'Binance_{binance_pair}_bid': [binance_bid_price],
        f'Binance_{binance_pair}_ask': [binance_ask_price],
        f'Deribit_{deribit_pair.replace("-", "")}_bid': [deribit_bid_price],
        f'Deribit_{deribit_pair.replace("-", "")}_ask': [deribit_ask_price],
        f'Bitget_{bitget_pair.replace("_", "")}_bid': [bitget_bid_price],
        f'Bitget_{bitget_pair.replace("_", "")}_ask': [bitget_ask_price]
    }

    df = pd.DataFrame(data_dict)

    csv_file = f"BTC_Deribit-Binance-Bitget - {interval} Sec.csv"

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

    df = pd.read_csv(f'BTC_Deribit-Binance-Bitget - {interval} Sec.csv')
    df = df[
        ['timestamp', 'Binance_BTCTUSD_bid', 'Binance_BTCTUSD_ask', 'Bitget_BTCUSDTUMCBL_bid', 'Bitget_BTCUSDTUMCBL_ask']]
    df['diff'] = df['Bitget_BTCUSDTUMCBL_ask'] - df['Binance_BTCTUSD_ask']
    df['adj_diff'] = df['diff'] * qty
    df['ma'] = df['adj_diff'].rolling(x).mean()
    df['sd'] = df['adj_diff'].rolling(x).std()
    df['z'] = (df['adj_diff'] - df['ma']) / df['sd']
    df['+b'] = df['ma'] + df['sd'] * y
    df['-b'] = df['ma'] - df['sd'] * y
    df['fee'] = df['Bitget_BTCUSDTUMCBL_ask'] * qty * 0.00002 * 2.8

    # df['pos'] = np.where(df['z'] > y, -1, 0)
    adj_diff = df['adj_diff'].iloc[-1]
    fee = df['fee'].iloc[-1]
    diff1 = float(df['+b'].iloc[-1])
    diff2 = float(df['-b'].iloc[-1])

    def pos():
        pos = 0
        if adj_diff - fee > 0:
            if adj_diff > diff1:
                pos = -1
            elif adj_diff < diff2:
                pos = 1
            elif diff2 < adj_diff < diff1:
                pos = 0
        else:
            print(f'fee > diff: fee = {fee}, diff = {adj_diff}')

        return pos

    pos = pos()
    print(f'Signal = {pos}')
    # print(type(pos)) #<class 'numpy.int32'>
    # print(pos)

    print(df.tail(5))

    # fetch Bybit / Binance position
    binance_balance = binance_request.get_account_info()
    print(f'Binance position: {binance_balance}')
    # bitget_all_position, holding_symbol, holding_side, holding_size = bitget_request.get_all_positions('umcbl')
    response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, marginCoin)
    print(f'Bitget position: symbol = {holding_symbol}, side = {holding_side}, size = {holding_size}')
    # print(holding_symbol) #BTCUSDT_UMCBL
    # print(holding_side) #long/ short
    # print(holding_size) #0.001(qty)

    # demo
    # {'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '199.00000000', 'AXS': '0.00500000', 'WOO': '7.05479750'}
    # {'side': 'Sell', 'symbol': 'USDCUSDT', 'size': '10.0'} / {'side': 'None', 'symbol': 'USDCUSDT', 'size': '0.0'}

    # RTQ

    # bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
    # diff_now = binance_ask_price - float(bitget_ask_price)

    # print(f'bybit bid = {bybit_bid_price}, ask = {bybit_ask_price}')

    # pos = 1

    ###### place order ######
    try:
        if pos == -1:
            # if previously == 1, pass
            if holding_size > '0':
                print('signal = -1, position = -1')
                pass


        # if there is no position, open new position
            elif holding_size == '0':
                bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)
                orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, marginCoin, 'limit',bitget_ask_price)
                counter = 0
                print('signal = -1, position = 0')
                print('long binance, short bitget')
                while counter < 5:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now >= diff1:
                            # Check if order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                response = binance_request.place_order(symbol='BTCTUSD', side='BUY',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Buy: {response}')
                                break
                            time.sleep(1)

                        elif diff_now < diff1:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                response = binance_request.place_order(symbol='BTCTUSD', side='BUY',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Buy: {response}')
                            else:
                                cancel_counter += 1
                            break

                        if counter == 5:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                response = binance_request.place_order(symbol='BTCTUSD', side='BUY',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Buy: {response}')
                            else:
                                cancel_counter += 1


                    except requests.exceptions.Timeout:
                        print("Request timed out. Retrying...")
                        continue

                    except Exception as e:
                        print(f'Error: {e}')
                        print('pos == 1, else dead')
                        pass

        if pos == 1:
            # if previously has no position, pass
            if holding_size == '0':
                print('signal = 1, position = 1 / 0')
                pass

            # if there is a position, settle it
            elif holding_size > '0':
                bitget_ask_price, bitget_bid_price = bitget_request.fetch_bitget_data(bitget_symbol)
                orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, marginCoin, 'limit', bitget_bid_price)
                counter = 0
                print('signal = -1, position = 0')
                print('short binance,long bitget')
                while counter < 5:
                    try:
                        diff_now = diff_rtq()
                        counter += 1
                        print(f'counter = {counter}')
                        if diff_now <= diff2:
                            # Check if order is executed
                            state, size, filledQty = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                            print(f'state = {state}')
                            if state in ['new', 'partially_filled']:
                                print(f'has open order:{orderid}')
                            else:
                                response = binance_request.place_order(symbol='BTCTUSD', side='SELL',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Sell: {response}')
                                break
                            time.sleep(1)

                        elif diff_now > diff2:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                response = binance_request.place_order(symbol='BTCTUSD', side='SELL',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Sell: {response}')
                            else:
                                cancel_counter += 1
                            time.sleep(1)
                            break


                        if counter == 5:
                            cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                            print(f'bitget cancel status = {cancel_status}')
                            if cancel_status == 'No order to cancel':
                                response = binance_request.place_order(symbol='BTCTUSD', side='SELL',
                                                                       order_type='MARKET', quantity=qty)  # BTC qty
                                order_counter += 1
                                print(f'Binance Market Sell: {response}')
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
            print('pos = 0, pass')


    except Exception as e:
        if "'NoneType' object is not subscriptable" in str(e):
            tg_pop(f'Bitget / Binance BTC error: {e},\n\n , code restarting')
            pass


    elapsed = time.time() - start_time
    print(f'elapsed = {elapsed}')
    if elapsed < 10:
        time.sleep(10 - elapsed)
    print('end')

    return order_counter, cancel_counter


###### Bitget Variable ######
bitget_symbol = 'BTCUSDT_UMCBL'
qty = 0.001
product_type = 'UMCBL'
marginCoin = 'USDT'
response = bitget_request.set_position_mode(product_type, 'single_hold')
print(response)

###### Binance Variable ######
binance_symbol = 'BTCTUSD'

###### Execution ######
counter = 0
cancel_counter = 0
order_counter = 0
interval = 10

######

response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, marginCoin)
print(f'Bitget position: symbol = {holding_symbol}, side = {holding_side}, size = {holding_size}')


time.sleep(1234)

######

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
        tg_pop(f'Binance / Bitget BTC error: {e},\n traceback: {traceback.format_exc()}')
        break

