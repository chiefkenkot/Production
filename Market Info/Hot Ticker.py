import ccxt
import time
import pandas as pd
import numpy as np
import datetime
from pprint import pprint
import pal
from pybit import usdt_perpetual
from pybit import spot
import requests


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


###### Request #######

url = 'https://api.bybit.com/v5/market/tickers'

# param = {'category': 'spot','symbol': 'MATICUSDT'}
param = {'category': 'spot'}

####### kick off to generate 'old_data.csv' ######
response = requests.get(url, params=param)

spot_list = response.json()['result']['list']
# pprint(spot_list)

df_new = pd.DataFrame.from_dict(spot_list)
df_new = df_new[['symbol', 'price24hPcnt']]

####### Extract Data to CSV #######
df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)
df_new.to_csv('old_data.csv', index=False)


####### Shortlisting #######
df_above_13 = df_new[df_new['price24hPcnt'] > '0.13']
symbol_above_13 = list(df_above_13['symbol'])

time.sleep(300)

####### Looping #######

pct_change = 0.13

while True:
    ###### Request Data ######
    response = requests.get(url, params=param)

    spot_list = response.json()['result']['list']

    df_new = pd.DataFrame.from_dict(spot_list)
    df_new = df_new[['symbol', 'price24hPcnt']]
    df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)

    ###### Buy List ######
    df_above_13 = df_new[df_new['price24hPcnt'] > str(pct_change)]
    symbol_above_13 = list(df_above_13['symbol'])
    # print(symbol_above_13)

    df_old = pd.read_csv('old_data.csv')
    df_old = df_old[df_old['price24hPcnt'] > pct_change]
    old_symbol_above_13 = list(df_old['symbol'])
    # print(old_symbol_above_13)

    buy_list = set(symbol_above_13) - set(old_symbol_above_13)
    # settle_list = set(old_symbol_above_13) - set(symbol_above_13)
    print(buy_list)


    ###### Sell List ######
    # df_below_13 = df_new[df_new['price24hPcnt'] < str(-pct_change)]
    # symbol_below_13 = list(df_below_13['symbol'])
    # print(symbol_below_13)
    #
    # df_old = pd.read_csv('old_data.csv')
    # df_old = df_old[df_old['price24hPcnt'] < -pct_change]
    # old_symbol_below_13 = list(df_old['symbol'])
    # print(old_symbol_below_13)
    #
    # sell_list = set(symbol_below_13) - set(old_symbol_below_13)
    # print(sell_list)

    ###### TG POP BUY ######
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    message = 'buy list:' + str(buy_list)
    requests.get(base_url + message)

    # ###### TG POP SELL ######
    # base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    # message = 'sell list:' + str(sell_list)
    # requests.get(base_url + message)

    # Save the new DataFrame to the CSV file
    df_new.to_csv('old_data.csv', index=False)

    # Wait for 5 minutes before making the next request
    time.sleep(300)


