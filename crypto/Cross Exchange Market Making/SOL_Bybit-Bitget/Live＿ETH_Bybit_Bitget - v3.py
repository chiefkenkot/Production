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
# bitget_api_key = pal.bitget_key
# bitget_secret_key = pal.bitget_secret
# bitget_pass_phrase = pal.bitget_pass_phrase
bitget_request = Bitget_Request(bitget_api_key, bitget_secret_key, bitget_pass_phrase)

# bybit_api_key = pal.hhyp_bybit_key_1
# bybit_api_secret = pal.hhyp_bybit_secret_1
# bybit_request = ByBitRequest(bybit_api_key, bybit_api_secret)

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

    deribit_pair = 'BTC-PERPETUAL'
    deribit_ask_price, deribit_bid_price = fetch_deribit_data(deribit_pair)

    bitget_pair = bitget_symbol
    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)

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

    csv_file = f'ETH_Deribit-Bybit-Bitget - {interval} Sec.csv'

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    # print(df)

    return data_dict


def ask_diff_rtq():
    # RTQ
    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
    bybit_ask_price, bybit_bid_price =bybit_request.fetch_bybit_data(bybit_symbol)
    ask_diff_now = round((bybit_ask_price - float(bitget_ask_price)), 2)

    return ask_diff_now


def bid_diff_rtq():
    # RTQ
    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
    bybit_ask_price, bybit_bid_price =bybit_request.fetch_bybit_data(bybit_symbol)
    bid_diff_now = round((bybit_bid_price - float(bitget_bid_price)), 2)

    return bid_diff_now

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
    ask_df = pd.read_csv(f'ETH_Deribit-Bybit-Bitget - {interval} Sec.csv')
    ask_df= ask_df[['timestamp', 'Bybit_ETHUSDC_ask', 'Bitget_ETHUSDTUMCBL_ask']]
    ask_df['ask_diff'] = ask_df['Bybit_ETHUSDC_ask'] - ask_df['Bitget_ETHUSDTUMCBL_ask']
    ask_df['ask_ma'] = ask_df['ask_diff'].rolling(x).mean()
    ask_df['ask_sd'] = ask_df['ask_diff'].rolling(x).std()
    ask_df['ask_z'] = (ask_df['ask_diff'] - ask_df['ask_ma']) / ask_df['ask_sd']
    ask_df['ask_+b'] = ask_df['ask_ma'] + ask_df['ask_sd'] * y
    ask_df['ask_-b'] = ask_df['ask_ma'] - ask_df['ask_sd'] * y
    ask_df['ask_pos'] = np.where(ask_df['ask_z'] > y, -1, np.where(ask_df['ask_z'] < -y, 1, 0))

    bid_df = pd.read_csv(f'ETH_Deribit-Bybit-Bitget - {interval} Sec.csv')
    bid_df = bid_df[['timestamp', 'Bybit_ETHUSDC_bid',  'Bitget_ETHUSDTUMCBL_bid']]
    bid_df['bid_diff'] = bid_df['Bybit_ETHUSDC_bid'] - bid_df['Bitget_ETHUSDTUMCBL_bid']
    bid_df['bid_ma'] = bid_df['bid_diff'].rolling(x).mean()
    bid_df['bid_sd'] = bid_df['bid_diff'].rolling(x).std()
    bid_df['bid_z'] = (bid_df['bid_diff'] - bid_df['bid_ma']) / bid_df['bid_sd']
    bid_df['bid_+b'] = bid_df['bid_ma'] + bid_df['bid_sd'] * y
    bid_df['bid_-b'] = bid_df['bid_ma'] - bid_df['bid_sd'] * y
    bid_df['bid_pos'] = np.where(bid_df['bid_z'] > y, -1, np.where(bid_df['bid_z'] < -y, 1, 0))

    pos = ask_df['ask_pos'].iloc[-1]
    diff1 = float(bid_df['bid_+b'].iloc[-1])
    # diff2 = float(bid_df['bid_-b'].iloc[-1])
    # diff3 = float(ask_df['ask_+b'].iloc[-1])
    diff4 = float(ask_df['ask_-b'].iloc[-1])
    # print(type(pos)) #<class 'numpy.int32'>
    # print(pos)
    print('======================================')
    print(ask_df.tail(3))
    print('======================================')
    print(bid_df.tail(3))
    print('======================================')

    # fetch Bybit / Binance position
    bybit_balance = bybit_request.get_wallet_balance('spot')
    print(f'Bybit position: {bybit_balance}')
    # bitget_all_position, holding_symbol, holding_side, holding_size = bitget_request.get_all_positions('umcbl')
    response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, marginCoin)
    print(f'Bitget position: symbol = {holding_symbol}, side = {holding_side}, size = {holding_size}')
    print('======================================')
    # print(holding_symbol) #BTCUSDT_UMCBL
    # print(holding_side) #long/ short
    # print(holding_size) #0.001(qty)

    # demo
    # {'BNB': '0.00773528', 'USDT': '0.95260036', 'TUSD': '199.00000000', 'AXS': '0.00500000', 'WOO': '7.05479750'}
    # {'side': 'Sell', 'symbol': 'USDCUSDT', 'size': '10.0'} / {'side': 'None', 'symbol': 'USDCUSDT', 'size': '0.0'}

    def transactions_data(pos, bybit_transaction, bitget_transaction):
        state, size, filledQty, bitget_fee = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
        data = {
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Bybit': [bybit_transaction],
            'Bitget': [bitget_transaction],
            'side': [pos],
            'fee': [bitget_fee]
        }
        df = pd.DataFrame(data)

        csv_file = f"Result_ETH_Deribit-Bybit-Bitget - {interval} Sec.csv"

        if not os.path.isfile(csv_file):
            df.to_csv(csv_file, mode="w", header=True, index=False)
        else:
            df.to_csv(csv_file, mode="a", header=False, index=False)

    ###### place order ######
    try:
        if pos == 1:
            # if previously == -1
            if holding_side == 'long' and holding_size > '0':
                bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                if ask_size < size_filter:
                    print(f'ask size = {ask_size} < {size_filter}')
                elif ask_size >= size_filter:
                    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                    orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty*2, marginCoin, 'limit', bitget_ask_price)
                    print('signal = 1, position = -1')
                    print('long bybit, short bitget')
                    start_time = time.time()
                    while True:
                        try:
                            elapsed_time = time.time() - start_time
                            ask_diff_now = ask_diff_rtq()
                            if elapsed_time <= (interval-3):
                                if ask_diff_now <= diff4:
                                    # Check if order is executed
                                    state, size, filledQty, bitget_fee = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                                    print(f'state = {state}')
                                    if state in ['new', 'partially_filled']:
                                        print(f'has open order:{orderid}')
                                    else:
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_ask_price + 2,
                                                                                                 qty=qty*2, is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Buy: {response}')
                                        print(f'Transaction price = {transaction_price}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_ask_price)
                                        break
                                    time.sleep(time_sleep)

                                elif ask_diff_now > diff4:
                                    cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                    print(f'bitget cancel status = {cancel_status}')
                                    if cancel_status == 'No order to cancel':
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_ask_price + 2,
                                                                                                 qty=qty * 2,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Buy: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_ask_price)
                                    else:
                                        cancel_counter += 1
                                    print(f'cancel reason = ask_diff_now {ask_diff_now} > ask-b {diff4}')
                                    break

                            elif elapsed_time > (interval-3):
                                cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                print(f'bitget cancel status = {cancel_status}')
                                if cancel_status == 'No order to cancel':
                                    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                    response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                             bybit_symbol, 'Limit',
                                                                                             price=bybit_ask_price + 2,
                                                                                             qty=qty * 2, is_leverage=0,
                                                                                             order_filter='order',
                                                                                             time_in_force='GTC')

                                    response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                  orderLinkId=orderlink_id)
                                    order_counter += 1
                                    print(f'Bybit Market Buy: {response}')
                                    transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                      bitget_transaction=bitget_ask_price)
                                else:
                                    cancel_counter += 1
                                print(f'cancel reason: loop elasped time > 12 ({elapsed_time})')
                                break

                        except requests.exceptions.Timeout:
                            print("Request timed out. Retrying...")
                            continue

                        except Exception as e:
                            print(f'Error: {e}')
                            print('pos == 1, elif dead')
                            break

        # if previously == 1, pass
            elif holding_side == 'short' and holding_size > '0':
                print('signal = 1, position = 1')

            # if there is no position, open new position
            else:
                bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                if ask_size < size_filter:
                    print(f'ask size = {ask_size} < {size_filter}')
                elif ask_size >= size_filter:
                    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                    orderid = bitget_request.place_single_order(bitget_symbol, 'sell_single', qty, marginCoin, 'limit', bitget_ask_price)
                    print('signal = 1, position = 0')
                    print('long Bybit, short bitget')
                    start_time = time.time()
                    while True:
                        try:
                            elapsed_time = time.time() - start_time
                            ask_diff_now = ask_diff_rtq()
                            if elapsed_time <= (interval-3):
                                if ask_diff_now <= diff4:
                                    # Check if order is executed
                                    state, size, filledQty, bitget_fee = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                                    print(f'state = {state}')
                                    if state in ['new', 'partially_filled']:
                                        print(f'has open order:{orderid}')
                                    else:
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_ask_price + 2,
                                                                                                 qty=qty, is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Buy: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_ask_price)
                                        break
                                    time.sleep(time_sleep)

                                elif ask_diff_now > diff4:
                                    cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                    print(f'bitget cancel status = {cancel_status}')
                                    if cancel_status == 'No order to cancel':
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_ask_price + 2,
                                                                                                 qty=qty,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Buy: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_ask_price)
                                    else:
                                        cancel_counter += 1
                                    print(f'cancel reason = ask_diff_now {ask_diff_now} > ask-b {diff4}')
                                    break

                            if elapsed_time > (interval-3):
                                cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                print(f'bitget cancel status = {cancel_status}')
                                if cancel_status == 'No order to cancel':
                                    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                    response, orderlink_id = bybit_request.place_limit_order('spot', 'Buy',
                                                                                             bybit_symbol, 'Limit',
                                                                                             price=bybit_ask_price + 2,
                                                                                             qty=qty, is_leverage=0,
                                                                                             order_filter='order',
                                                                                             time_in_force='GTC')

                                    response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                  orderLinkId=orderlink_id)
                                    order_counter += 1
                                    print(f'Bybit Market Buy: {response}')
                                    transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                      bitget_transaction=bitget_ask_price)
                                else:
                                    cancel_counter += 1
                                print(f'cancel reason: loop elasped time > 12 ({elapsed_time})')
                                break


                        except requests.exceptions.Timeout:
                            print("Request timed out. Retrying...")
                            continue

                        except Exception as e:
                            print(f'Error: {e}')
                            print('pos == 1, else dead')
                            break

        if pos == -1:
            # if previously == 1
            if holding_side == 'short' and holding_size > '0':
                bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                if bid_size < size_filter:
                    print(f'bid size = {bid_size} < {size_filter}')
                elif bid_size >= size_filter:
                    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                    orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty*2, marginCoin, 'limit', bitget_bid_price)
                    print('signal = -1, position = 1')
                    print('short Bybit,long bitget')
                    start_time = time.time()
                    while True:
                        try:
                            elapsed_time = time.time() - start_time
                            bid_diff_now = bid_diff_rtq()
                            if elapsed_time <= (interval-3):
                                if bid_diff_now >= diff1:
                                    # Check if order is executed
                                    state, size, filledQty, bitget_fee = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                                    print(f'state = {state}')
                                    if state in ['new', 'partially_filled']:
                                        print(f'has open order:{orderid}')
                                    else:
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_bid_price - 2,
                                                                                                 qty=qty * 2,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Sell: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_bid_price)
                                        break
                                    time.sleep(time_sleep)

                                elif bid_diff_now < diff1:
                                    cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                    print(f'bitget cancel status = {cancel_status}')
                                    if cancel_status == 'No order to cancel':
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_bid_price - 2,
                                                                                                 qty=qty * 2,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Sell: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_bid_price)
                                    else:
                                        cancel_counter += 1
                                    print(f'cancel reason = bid_diff_now {bid_diff_now} < bid_+b {diff1}')
                                    break

                            if elapsed_time > (interval-3):
                                cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                print(f'bitget cancel status = {cancel_status}')
                                if cancel_status == 'No order to cancel':
                                    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                    response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                             bybit_symbol, 'Limit',
                                                                                             price=bybit_bid_price - 2,
                                                                                             qty=qty * 2,
                                                                                             is_leverage=0,
                                                                                             order_filter='order',
                                                                                             time_in_force='GTC')

                                    response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                  orderLinkId=orderlink_id)
                                    order_counter += 1
                                    print(f'Bybit Market Sell: {response}')
                                    transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                      bitget_transaction=bitget_bid_price)
                                else:
                                    cancel_counter += 1
                                print(f'loop elasped time > 12: {elapsed_time}')
                                break


                        except requests.exceptions.Timeout:
                            print("Request timed out. Retrying...")
                            continue

                        except Exception as e:
                            print(f'Error: {e}')
                            print('pos == -1, elif dead')
                            break

            # if previously == -1, pass
            elif holding_side == 'long' and holding_size > '0':
                print('signal = -1, position = -1')


            # if there is no position, open new position
            else:
                bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                if bid_size < size_filter:
                    print(f'bid size = {bid_size} < {size_filter}')

                elif bid_size >= size_filter:
                    bitget_ask_price, bitget_bid_price, ask_size, bid_size = bitget_request.fetch_bitget_data(bitget_symbol)
                    orderid = bitget_request.place_single_order(bitget_symbol, 'buy_single', qty, marginCoin, 'limit',bitget_bid_price)
                    print('signal = -1, position = 0')
                    print('short Bybit,long bitget')
                    start_time = time.time()  # record the start time
                    while True:
                        try:
                            elapsed_time = time.time() - start_time
                            bid_diff_now = bid_diff_rtq()
                            if elapsed_time <= (interval-3):
                                if bid_diff_now >= diff1:
                                    # Check if order is executed
                                    state, size, filledQty, bitget_fee = bitget_request.get_order_detail(bitget_symbol, order_id=orderid)
                                    print(f'state = {state}')
                                    if state in ['new', 'partially_filled']:
                                        print(f'has open order:{orderid}')
                                    else:
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_bid_price - 2,
                                                                                                 qty=qty,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Sell: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_bid_price)
                                        break
                                    time.sleep(time_sleep)

                                elif bid_diff_now < diff1:
                                    cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                    print(f'bitget cancel status = {cancel_status}')
                                    if cancel_status == 'No order to cancel':
                                        bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                        response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                                 bybit_symbol, 'Limit',
                                                                                                 price=bybit_bid_price - 2,
                                                                                                 qty=qty,
                                                                                                 is_leverage=0,
                                                                                                 order_filter='order',
                                                                                                 time_in_force='GTC')

                                        response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                      orderLinkId=orderlink_id)
                                        order_counter += 1
                                        print(f'Bybit Market Sell: {response}')
                                        transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                          bitget_transaction=bitget_bid_price)
                                    else:
                                        cancel_counter += 1
                                    print(f'cancel reason = bid_diff_now {bid_diff_now} < bid_+b {diff1}')
                                    break


                            if elapsed_time > (interval-3):
                                cancel_status = bitget_request.cancel_all_orders(bitget_symbol, marginCoin)
                                print(f'bitget cancel status = {cancel_status}')
                                if cancel_status == 'No order to cancel':
                                    bybit_ask_price, bybit_bid_price = bybit_request.fetch_bybit_data(bybit_symbol)
                                    response, orderlink_id = bybit_request.place_limit_order('spot', 'Sell',
                                                                                             bybit_symbol, 'Limit',
                                                                                             price=bybit_bid_price - 2,
                                                                                             qty=qty,
                                                                                             is_leverage=0,
                                                                                             order_filter='order',
                                                                                             time_in_force='GTC')

                                    response, transaction_price = bybit_request.get_order_history('spot',
                                                                                                  orderLinkId=orderlink_id)
                                    order_counter += 1
                                    print(f'Bybit Market Sell: {response}')
                                    transactions_data(pos=pos, bybit_transaction=transaction_price,
                                                      bitget_transaction=bitget_bid_price)
                                else:
                                    cancel_counter += 1
                                print(f'loop elasped time > 12: {elapsed_time}')
                                break


                        except requests.exceptions.Timeout:
                            print("Request timed out. Retrying...")
                            continue

                        except Exception as e:
                            print(f'Error: {e}')
                            print('pos == -1, elif dead')
                            break

        if pos == 0:
            print('signal = 0, pass')


    except Exception as e:
        if "'NoneType' object is not subscriptable" in str(e):
            tg_pop(f'Bitget / Bybit BTC error: {e},\n\n , code restarting')
        else:
            pass


    elapsed = time.time() - start_time
    print(f'elapsed = {elapsed}')
    if elapsed < interval:
        time.sleep(interval - elapsed)
    print('end')

    return order_counter, cancel_counter
    # time.sleep(1234)


###### Bitget Variable ######
bitget_symbol = 'ETHUSDT_UMCBL'
qty = 0.01
product_type = 'UMCBL'
marginCoin = 'USDT'
response = bitget_request.set_position_mode(product_type, 'single_hold')
print(response)

# time.sleep(1234)
###### Bybit Variable ######
bybit_symbol = 'ETHUSDC'
# bybit_symbol = 'USDCUSDT'
category = 'spot'


###### Execution ######
counter = 0
cancel_counter = 0
order_counter = 0
interval = 15
time_sleep = 0.1
size_filter = 25


bybit_balance = bybit_request.get_wallet_balance('spot')
print(f'Bybit position: {bybit_balance}')

response, holding_symbol, holding_side, holding_size = bitget_request.get_symbol_position_v2(bitget_symbol, marginCoin)
print(f'Bitget position: symbol = {holding_symbol}, side = {holding_side}, size = {holding_size}')

# time.sleep(2134)

# bitget_request.get_order_detail(bitget_symbol, 1071697845636714498)

# time.sleep(1234)

while True:
    try:
        if counter < 51:
            merged_data_dict = fetch_and_append_data_merged(interval=interval)
            counter += 1
            print(f'accumulating data {counter}')
            time.sleep(interval)

        else:
            merged_data_dict = fetch_and_append_data_merged(interval=interval)
            order_counter, cancel_counter = base(50, 0.6, cancel_counter, order_counter, interval)
            print(f'order counter = {order_counter}')
            print(f'cancel counter = {cancel_counter}')


    except ConnectionError as e:
        if 'Connection aborted' in str(e):
            continue
        else:
            raise

    except Exception as e:
        print(f'error: {e}')
        import traceback
        print(traceback.format_exc())
        tg_pop(f'Bybit / Bitget ETH error: {e},\n traceback: {traceback.format_exc()}')
        break

