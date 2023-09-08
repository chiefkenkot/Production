import time
import requests
from pybit import spot
from pprint import pprint


session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com", api_key='NWTXOQRFKVAIYEIRWP', api_secret='ESIFNPZRBREBACVQAAATLDWYMDQUIETIRCFD'
)


###### Trade History ######
def buy_pop():
    trade_record = session_unauth.user_trade_records(
                symbol='USDCUSDT',
                limit='1'
       )

    trade_record_temp = trade_record['result'][0]

    symbol = trade_record_temp['symbol']
    price = trade_record_temp['price']
    qty = trade_record_temp['qty']
    buy_record = ('Side: Buy','Symbol:', symbol,'Price:', price, 'Qty:', qty)
    print(buy_record)


    ###### TG POP ######

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = str(buy_record)

    requests.get(base_url+message)


def sell_pop():
    trade_record = session_unauth.user_trade_records(
                symbol='USDCUSDT',
                limit='1'
       )

    trade_record_temp = trade_record['result'][0]

    symbol = trade_record_temp['symbol']
    price = trade_record_temp['price']
    qty = trade_record_temp['qty']
    sell_record = ('Side: Sell','Symbol:', symbol,'Price:', price, 'Qty:', qty)
    print(sell_record)


    ###### TG POP ######

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = str(sell_record)

    requests.get(base_url+message)


