import time
import requests
from pybit import spot
from pprint import pprint
from pybit import usdt_perpetual

session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
price_quote = (session_unauth.public_trading_records(
            symbol="APEUSDT",
            limit=1
            ))
price_quote = price_quote['result'][0]['price']
# print(price_quote)

###### TG POP ######

def tg_pop_long():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Open Long @') + str(price_quote)

    requests.get(base_url+message)

tg_pop_long()


def tg_pop_short():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Open Short @') + str(price_quote)

    requests.get(base_url+message)


def tg_pop_settle_long():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Settle Long @') + str(price_quote)

    requests.get(base_url+message)


def tg_pop_settle_short():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Settle Short @') + str(price_quote)

    requests.get(base_url+message)


def tg_pop_reverse_to_long():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Reverse to Long @') + str(price_quote)

    requests.get(base_url+message)


def tg_pop_reverse_to_short():

    session_unauth = usdt_perpetual.HTTP(endpoint="https://api.bybit.com")
    price_quote = (session_unauth.public_trading_records(
        symbol="APEUSDT",
        limit=1
    ))
    price_quote = price_quote['result'][0]['price']

    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = ('Reverse to Short @') + str(price_quote)

    requests.get(base_url+message)


