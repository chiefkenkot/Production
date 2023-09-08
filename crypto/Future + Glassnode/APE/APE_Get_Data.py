import ccxt
import time
import pandas as pd
import datetime
from pprint import pprint
import pal
from pybit import usdt_perpetual

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# print(datetime.datetime.now())
# time.sleep(1234)

rtq_info = {'DateTime':[], 'close':[]}

# if datetime.datetime.minute == 9 and datetime.datetime.second == 55:

while True:
    # if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 0:
    if datetime.datetime.now().second == 0:

        session_unauth = usdt_perpetual.HTTP(
            endpoint="https://api.bybit.com"
        )
        price_quote = (session_unauth.public_trading_records(
            symbol="APEUSDT",
            limit=1
        ))

        price_quote = price_quote['result'][0]['price']

        col = ['DateTime', 'close']
        rtq_info['DateTime'].append(datetime.datetime.now())
        rtq_info['close'].append(price_quote)
        df = pd.DataFrame(rtq_info, columns=col)

        df.to_csv('data.csv', mode='w', index=False, header=True)
        print(datetime.datetime.now())
        time.sleep(555)
