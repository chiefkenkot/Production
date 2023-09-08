import datetime
import schedule
from pybit import spot
import pandas as pd
import time
from pprint import pprint


session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com", api_key='NWTXOQRFKVAIYEIRWP', api_secret='ESIFNPZRBREBACVQAAATLDWYMDQUIETIRCFD'
)

###### bid-ask reading ######

symbol = 'MATICUSDT'

session_unauth.symbol = symbol

# bids_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidPrice']
# bidQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidQty']
# asks_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askPrice']
# askQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askQty']

# print('ask=', asks_bybit, 'qty=', askQty_bybit)
# print('bid=', bids_bybit, 'qty=', bidQty_bybit)
# time.sleep(1234)


###### Sub ac balance Market Maker ######

# wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])
# wallet_balance = wallet_balance[1]['free']
# wallet_has_usdt = wallet_balance[1]['free']

# print(wallet_has_usdt)
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


###### Buy and Sell Trigers ######

# quantity = round((float(wallet_balance) / float(asks_bybit))*0.95, 2)
# print(quantity)
# time.sleep(1234)



def sniper():
    while True:
        ###### RTQ + Wallet #####

        session_unauth = spot.HTTP(
            endpoint="https://api.bybit.com", api_key='NWTXOQRFKVAIYEIRWP',
            api_secret='ESIFNPZRBREBACVQAAATLDWYMDQUIETIRCFD'
        )
        session_unauth.symbol = symbol

        bids_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidPrice']
        bidQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidQty']
        asks_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askPrice']
        askQty_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askQty']

        print('ask=', asks_bybit, 'qty=', askQty_bybit)
        print('bid=', bids_bybit, 'qty=', bidQty_bybit)

        wallet_balance = (session_unauth.query_account_info()['result']['loanAccountList'])
        wallet_balance = wallet_balance[1]['free']


        ###### Order Function ######
        quantity = round((float(wallet_balance) / float(asks_bybit)) * 0.1, 2)

        def place_marketbuy_order():

            session_unauth.place_active_order(
                symbol=symbol,
                side='Buy',
                type='MARKET',
                qty=quantity,  # need to adjust '-x' if the qty change!
                # qty=1, #need to adjust '-x' if the qty change!
                timeInForce='GTC',
                price=asks_bybit
            )


        ###### Logic ######
        try:
            place_marketbuy_order()
        except:
            continue


schedule.every().day.at('23:05').do(sniper)

while True:
    schedule.run_pending()
    time.sleep(1)
