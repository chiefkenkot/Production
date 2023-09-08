from pybit import spot
import pandas as pd
import time
from pprint import pprint
import TG_Pop_Up


session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com", api_key='NWTXOQRFKVAIYEIRWP', api_secret='ESIFNPZRBREBACVQAAATLDWYMDQUIETIRCFD'
)

###### bid-ask reading ######


session_unauth.symbol = 'USDCUSDT'

bids_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['bidPrice']
bidQty_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['bidQty']
asks_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['askPrice']
askQty_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['askQty']

# print('ask=', asks_bybit, 'qty=', askQty_bybit)
# print('bid=', bids_bybit, 'qty=', bidQty_bybit)






###### Sub ac balance Market Maker ######

wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])
# wallet_balance = wallet_balance[0]['free']
# pprint(wallet_balance)


# while True:
#     wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])
#     x = wallet_balance[0]['free']
#     y = '20'
#
#     if wallet_balance[0]['tokenId'] == 'USDT' and x > y:
#         print('s1')
#
#     elif wallet_balance[0]['tokenId'] == 'USDT' and x < y:
#         print('s2')
#
#     time.sleep(5)


time.sleep(1234)

# {'free': '10.001',
#   'interest': '0',
#   'loan': '0',
#   'locked': '0',
#   'tokenId': 'USDT',
#   'total': '10.001'},
#  {'free': '0',
#   'interest': '0',
#   'loan': '0',
#   'locked': '0',
#   'tokenId': 'USDC',
#   'total': '0'}

###### Buy and Sell Trigers ######
def place_buy_order():

    session_unauth.place_active_order(
        symbol='USDCUSDT',
        side='Buy',
        type='LIMIT',
        qty=round(float(wallet_balance[0]['free']), 1)-0.1, #need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=bids_bybit
    )

def place_sell_order():

    session_unauth.place_active_order(
        symbol='USDCUSDT',
        side='Sell',
        type='LIMIT',
        qty=round(float(wallet_balance[1]['free']), 1) -0.1, #need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=asks_bybit
    )

def cancel_order():
    session_unauth.batch_cancel_active_order(
        symbol='USDCUSDT',
        orderTypes='LIMIT,LIMIT_MAKER'
    )


# def place_marketsell_order():
#
#     session_unauth.place_active_order(
#         symbol='USDCUSDT',
#         side='Sell',
#         type='MARKET',
#         qty=round(float(wallet_balance[1]['locked']), 1) -0.1, #need to adjust '-x' if the qty change!
#         timeInForce='GTC',
#         price=bids_bybit
#      )

def place_marketsell_order():
    session_unauth.place_active_order(
        symbol='USDCUSDT',
        side='Sell',
        type='LIMIT',
        qty=round(float(wallet_balance[1]['locked']), 2),  # need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=bids_bybit
        )


def place_marketbuy_order():

    session_unauth.place_active_order(
        symbol='USDCUSDT',
        side='Buy',
        type='LIMIT',
        qty=round(float(wallet_balance[0]['locked']), 1), #need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=asks_bybit
     )



while True:
    ###### RTQ + Wallet #####
    session_unauth.symbol = 'USDCUSDT'

    bids_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['bidPrice']
    bidQty_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['bidQty']
    asks_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['askPrice']
    askQty_bybit = session_unauth.best_bid_ask_price(symbol="USDCUSDT")['result']['askQty']

    print('ask=', asks_bybit, 'qty=', askQty_bybit)
    print('bid=', bids_bybit, 'qty=', bidQty_bybit)

    wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])

    ###### Q status check ######
    is_usdt = wallet_balance[0]['tokenId'] == 'USDT'
    wallet_has_usdt = wallet_balance[0]['free'] > '0.1'
    has_usdt_line_up = wallet_balance[0]['locked'] > '1'

    is_usdc = wallet_balance[1]['tokenId'] == 'USDC'
    wallet_has_usdc = (wallet_balance[1]['free']) > '0.1'
    has_usdc_line_up = wallet_balance[1]['locked'] > '1'

    ###### Logic ######
    #1. If Bid>100k
    # 1.1 if wallet has USDT, then line up at bid     (cal ratio?/ bid>ask)
    if bidQty_bybit > '50000' and is_usdt and wallet_has_usdt:
        place_buy_order()
        TG_Pop_Up.sell_pop()

    # #1.2 if wallet has USDC, then line up at ask    (cal ratio?/ bid>ask)
    if bidQty_bybit > '50000' and is_usdc and wallet_has_usdc:
        place_sell_order()
        TG_Pop_Up.buy_pop()

    #1.3 if price move up and have available queue
    if bidQty_bybit > '50000' and askQty_bybit < '50000' and has_usdt_line_up:
        cancel_order()
        place_marketbuy_order() #print result later
        TG_Pop_Up.buy_pop()

    #2. If Bid<100k, cancel all order and sell
    if bidQty_bybit < '50000' and has_usdc_line_up:
        cancel_order()
        place_marketsell_order()
        TG_Pop_Up.sell_pop()

    #3. If price moved without any trigger
    # if has_usdt_line_up or has_usdc_line_up:
        #price line up now is not bid/ask price

    time.sleep(10)


###### Failed Case ######

# ask= 1.0003 qty= 1010932.76
# bid= 1.0002 qty= 848818.77
# ('Side: Buy', 'Symbol:', 'USDCUSDT', 'Price:', '1.0002', 'Qty:', '9.8') chased
# ask= 1.0003 qty= 1010922.96
# bid= 1.0002 qty= 796368.85
# ('Side: Buy', 'Symbol:', 'USDCUSDT', 'Price:', '1.0003', 'Qty:', '9.8') line up and sell
# ask= 1.0003 qty= 1010932.76
# bid= 1.0002 qty= 844463.57

# call back
# {'ext_code': None,
#  'ext_info': None,
#  'result': {'askPrice': '1.0003',
#             'askQty': '1000493.17',
#             'bidPrice': '1.0002',
#             'bidQty': '794053.29',
#             'symbol': 'USDCUSDT',
#             'time': 1672757952495},
#  'ret_code': 0,
#  'ret_msg': ''}