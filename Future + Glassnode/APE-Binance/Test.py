import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time
from binance.client import Client
import pal_binance

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

client = Client(pal_binance.API_Key, pal_binance.API_Secret)

symbol_usdt = 'APEUSDT'

###### Draw Data ######
# Time Param: https://python-binance.readthedocs.io/en/latest/constants.html
# candles = client.get_klines(symbol='APEUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)

klines = client.get_historical_klines(symbol_usdt, Client.KLINE_INTERVAL_15MINUTE, "12 May, 2020", "25 Jan, 2023")
# klines = client.get_historical_klines(symbol_usdt, Client.KLINE_INTERVAL_1HOUR, "12 May, 2020", "25 Jan, 2023")
# klines = client.get_historical_klines(symbol_usdt, Client.KLINE_INTERVAL_4HOUR, "12 May, 2020", "25 Jan, 2023")
# klines = client.get_historical_klines(symbol_usdt, Client.KLINE_INTERVAL_1HOUR, "12 May, 2020", "25 Jan, 2023")

###### Data Frame ######
csv_name = 'APE_data_1h.csv'
# col = ['Date', 'open', 'high', 'low', 'value', 'volume', 'close time', 'Quote asset volume', 'Num trades', 'buy vol', 'buy asset volume', 'ignore.']
# df = pd.DataFrame(klines, columns=col)
# df = df[['Date', 'open', 'high', 'low', 'value']]
# df.to_csv(csv_name, mode='w', index=False, header=True)
# print(df)
#
# time.sleep(1234)

### Read CSV ###
# df = pd.read_csv(csv_name)
df = pd.read_csv(csv_name)
# df = pd.read_csv(csv_name)
df = df[['Date', 'open', 'high', 'low', 'value']]
df['pct_change'] = df['value'].pct_change()

high = df['high']
low = df['low']
close = df['value']

# x = 14
# y = 1

def ATR(x,y):
    df['average_high'] = df['high'].rolling(x).mean()
    df['average_low'] = df['low'].rolling(x).mean()

    ### ATR Calculation ###
    high_low = abs(high - low)
    high_close = abs(high - close.shift(-1))
    low_close = abs(low - close.shift(-1))
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(y).sum() / y

    # df['pos'] = np.where(df['value'] > df['average_high'], 1, np.where(df['value'] < df['average_low'], -1, 0))

    ### Logic ###
    def pos():

        # if break up, take 1 position
        # after open position,every 1/2 ATR add 1 position until 4
        while df['pos'] >=1 and df['pos'] <4:
            if df['value'] > df['value'].shift(1) + (atr * 0.25):
                df['pos'] += 1
            # if draw back 2 ATR, settle all position
            elif df['value'] < df['value'].shift(1) + (atr * 2):
                df['pos'] = 0

        # if break down, short 1 position
        # after open position, every 1/2 ATR add 1 short position until 4
        while df['pos'] <=-1 and df['pos'] >-4:
            if df['value'] < df['value'].shift(1) + (atr * 0.25):
                df['pos'] -= 1
            # if draw back 2 ATR, settle all position
            elif df['value'] > df['value'].shift(1) + (atr * 2):
                df['pos'] = 0


        return df['pos']

    pos()

    df['pos_t-1'] = df['pos'].shift(1)
    df['trade'] = abs(df['pos_t-1'] - df['pos'])
    df['cost'] = df['trade'] *0.05/100
    df['pnl'] = df['pos_t-1'] * df['pct_change'] - df['cost']
    df['cumu'] = df['pnl'].cumsum()

    df['bnh_pnl'] = df['pct_change']
    df.loc[0:x-1,'bnh_pnl'] = 0
    df['bnh_cumu'] = df['bnh_pnl'].cumsum()

    # sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24*4) ## 15m
    sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24) ## 1hr
    # sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*6) ## 4hr
    sharpe = round(sharpe,2)

    ### buy and hold sharpe
    # bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24*4) ## 15m
    bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365 * 24)  ## 1hr
    # bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*6) ## 4hr
    bnh_sharpe = round(bnh_sharpe, 2)

    # annual_return = round(df['pnl'].mean() * (365*24*4), 2) ## 15m
    annual_return = round(df['pnl'].mean() * (365 * 24), 2)  ## 1hr
    # annual_return = round(df['pnl'].mean() * (365*6), 2) ## 4hr

    df['dd'] = df['cumu'].cummax() - df['cumu']
    mdd = round(df['dd'].max(), 3)
    calmar = round(annual_return / mdd, 2)

    print(df.head(100))
    print(x, y, 'sharpe', sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)

    return pd.Series([x, y, sharpe], index=['x', 'y', 'sharpe'])

ATR(20,20)
time.sleep(1234)

########## optimization zone ##########

# ma_list = np.arange(5,105,5)
# # thres_list = np.arange(0.01,0.1,0.01)
# thres_list = np.arange(0,3,1)
#
# result_df = pd.DataFrame(columns=['x','y','sharpe'])
#
# for x in ma_list:
#     for y in thres_list:
#         ATR(x,y)
#         result_df = result_df.append(ATR(x,y), ignore_index=True)
#
# result_df = result_df.sort_values(by='sharpe', ascending=False)
# print(result_df)
#
# data_table = result_df.pivot(index='x',columns='y',values='sharpe')
# sns.heatmap(data_table, annot=True, fmt='g', cmap='Greens')
# plt.show()

########## backtesting zone ##########

### parameters
# x = 30
# y = 0.01
# # ma_diff(x,y)
# bband(x,y)
# fig = px.line(df, x='Date', y=['cumu','dd','bnh_cumu'], title='strategy')
# fig.show()