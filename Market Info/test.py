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
import matplotlib.pyplot as plt


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

df_new = pd.DataFrame.from_dict(spot_list)
df_new = df_new[['symbol', 'price24hPcnt']]

####### Extract Data to CSV #######
df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)
df_new.to_csv('old_data.csv', index=False)


####### Shortlisting #######
df_above_13 = df_new[df_new['price24hPcnt'] > '0.13']
symbol_above_13 = list(df_above_13['symbol'])

# print(df_above_13)
# print(symbol_above_13)

# list_1 = ['GPTUSDT', 'VRAUSDT', 'BTC3LUSDT', 'BLURUSDT', 'BONKUSDT', 'TUSDT', 'FTM2LUSDT', 'HOOKUSDT', 'CAPSUSDT']
#
# list_2 = ['GPTUSDT', 'VRAUSDT', 'BLURUSDT', 'BTC3LUSDT', 'TUSDT', 'BONKUSDT', 'FTM2LUSDT', 'BTCUSDT', 'CAPSUSDT']
#
# diff_1 = set(list_1) - set(list_2)
# diff_2 = set(list_2) - set(list_1)

# print(diff_1)
# print(diff_2)
time.sleep(100)

####### Looping #######

while True:
    response = requests.get(url, params=param)

    spot_list = response.json()['result']['list']

    df_new = pd.DataFrame.from_dict(spot_list)
    df_new = df_new[['symbol', 'price24hPcnt']]
    df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)

    #plot normal distribution
    data = df_new['price24hPcnt']
    mean = np.mean(data)
    std_dev = np.std(data)

    x = np.linspace(min(data), max(data), len(data))
    y = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-(x - mean) ** 2 / (2 * std_dev ** 2))

    plt.plot(x, y, color='blue')
    plt.hist(data, bins=10, density=True, alpha=0.5, color='cyan')
    plt.xlabel('Price24hPcnt')
    plt.ylabel('Probability density')
    plt.title('Normal Distribution of Price24hPcnt')
    plt.show()


    # Filter the DataFrame to show symbols with price24hPcnt above 0.13
    df_above_13 = df_new[df_new['price24hPcnt'] > '0.13']
    symbol_above_13 = list(df_above_13['symbol'])

    print(symbol_above_13)

    df_old = pd.read_csv('old_data.csv')
    df_old = df_old[df_old['price24hPcnt'] > 0.13]
    old_symbol_above_13 = list(df_old['symbol'])
    print(old_symbol_above_13)

    buy_list = set(symbol_above_13) - set(old_symbol_above_13)
    # settle_list = set(old_symbol_above_13) - set(symbol_above_13)

    print(buy_list)
    # print(settle_list)

    # Save the new DataFrame to the CSV file
    df_above_13.to_csv('old_data.csv', index=False)

    # Wait for 5 minutes before making the next request
    time.sleep(10)



