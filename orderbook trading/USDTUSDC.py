from pybit import spot
import pandas as pd
import time
from pprint import pprint
import TG_Pop_Up


session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com", api_key='NWTXOQRFKVAIYEIRWP', api_secret='ESIFNPZRBREBACVQAAATLDWYMDQUIETIRCFD'
)

###### bid-ask reading ######

symbol = 'USDCUSDT'

session_unauth.symbol = symbol

bids_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidPrice']
bidQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidQty']
asks_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askPrice']
askQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askQty']

# print('ask=', asks_bybit, 'qty=', askQty_bybit)
# print('bid=', bids_bybit, 'qty=', bidQty_bybit)






###### Sub ac balance Market Maker ######

wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])
# wallet_balance = wallet_balance[2]['free']

# pprint(wallet_balance)
# time.sleep(1234)

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


# time.sleep(1234)

# [{'free': '0.00461',
#   'interest': '0',
#   'loan': '0',
#   'locked': '0',
#   'remainAmount': '0',
#   'tokenId': 'MATIC',
#   'total': '0.00461'},
#  {'free': '7.696492048',
#   'interest': '0',
#   'loan': '0',
#   'locked': '0',
#   'remainAmount': '0',
#   'tokenId': 'USDT',
#   'total': '7.696492048'},
#  {'free': '0.0002',
#   'interest': '0',
#   'loan': '0',
#   'locked': '0',
#   'remainAmount': '0',
#   'tokenId': 'USDC',
#   'total': '0.0002'}]

###### Buy and Sell Trigers ######
def place_buy_order():

    session_unauth.place_active_order(
        symbol=symbol,
        side='Buy',
        type='LIMIT',
        qty=round(float(wallet_balance[1]['free']), 2) -0.01, #need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=0.9999
    )

def place_sell_order():

    session_unauth.place_active_order(
        symbol=symbol,
        side='Sell',
        type='LIMIT',
        qty=round(float(wallet_balance[2]['free']), 2) -0.01, #need to adjust '-x' if the qty change!
        timeInForce='GTC',
        price=1.0001
    )

def cancel_order():
    session_unauth.batch_cancel_active_order(
        symbol=symbol,
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

# def place_marketsell_order():
#     session_unauth.place_active_order(
#         symbol=symbol,
#         side='Sell',
#         type='LIMIT',
#         qty=round(float(wallet_balance[1]['locked']), 2),  # need to adjust '-x' if the qty change!
#         timeInForce='GTC',
#         price=bids_bybit
#         )
#
#
# def place_marketbuy_order():
#
#     session_unauth.place_active_order(
#         symbol=symbol,
#         side='Buy',
#         type='LIMIT',
#         qty=round(float(wallet_balance[0]['locked']), 1), #need to adjust '-x' if the qty change!
#         timeInForce='GTC',
#         price=asks_bybit
#      )



while True:
    ###### RTQ + Wallet #####
    symbol = 'USDCUSDT'

    session_unauth.symbol = symbol

    bids_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidPrice']
    bidQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidQty']
    asks_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askPrice']
    askQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askQty']

    print('ask=', asks_bybit, 'qty=', askQty_bybit)
    print('bid=', bids_bybit, 'qty=', bidQty_bybit)

    wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])

    ###### Q status check ######
    is_usdt = wallet_balance[1]['tokenId'] == 'USDT'
    usdt_balance = wallet_balance[1]['free']
    wallet_has_usdt = usdt_balance > '0.1'
    has_usdt_line_up = wallet_balance[1]['locked'] > '1'

    is_usdc = wallet_balance[2]['tokenId'] == 'USDC'
    usdc_balance = wallet_balance[2]['free']
    wallet_has_usdc = usdc_balance > '0.1'
    has_usdc_line_up = wallet_balance[2]['locked'] > '1'

    ###### Logic ######
    # 1. if wallet has USDT, then line up at bid 0.9999    (cal ratio?/ bid>ask)
    if wallet_has_usdt:
        print('USDT:', usdt_balance)
        place_buy_order()

    # 2. if wallet has USDC, then line up at ask 1.0001
    if wallet_has_usdc:
        print('USDC:',usdc_balance)
        place_sell_order()

    else:
        print('USDT:', usdt_balance)
        print('USDC:',usdc_balance)
        print('waiting')

    time.sleep(5)




