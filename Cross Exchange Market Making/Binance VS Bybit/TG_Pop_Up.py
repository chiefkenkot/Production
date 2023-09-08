import time
import requests
from pybit import spot
from pprint import pprint
from pybit import usdt_perpetual

###### Bybit Price Quote ######
# session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
# price_quote = (session_unauth.public_trading_records(
#             symbol="APEUSDT",
#             limit=1
#             ))
# price_quote = price_quote['result'][0]['price']
# print(price_quote)

###### TG POP ######

def tg_pop():

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('HHYP just buy BUSD')

    requests.get(base_url+message)


tg_pop()


