import time

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df = pd.read_csv('BTC_Bybit-Binance_Data.csv')
# df = df[['timestamp','Binance_BTCTUSD', 'Bybit_BTCUSDT']]
df = df[['timestamp','Binance_BTCTUSD_Ask', 'Binance_BTCTUSD_Bid', 'Bybit_BTCUSDC_Ask', 'Bybit_BTCUSDC_Bid']]


###### Fee Version ######

# def base():
#
#     df['extend_spread'] = df['Binance_BTCTUSD_Bid'] - df['Bybit_BTCUSDC_Ask']
#     df['contract_spread'] = df['Binance_BTCTUSD_Ask'] - df['Bybit_BTCUSDC_Bid']
#     # df['ask_spread'] =  df['Bybit_BTCUSDC_Ask'] - df['Binance_BTCTUSD_Ask']
#     # df['bid_spread'] = df['Bybit_BTCUSDC_Bid'] - df['Binance_BTCTUSD_Bid']
#
#
#     # df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))
#     df['pos'] = np.where(df['extend_spread'] > 1, -1, np.where(df['contract_spread'] < -1, 1, 0))
#     df['pos_change'] = df['pos'].diff()
#
#     # df['entry_price'] = np.where(df['pos_change'] != 0, df['diff'], np.nan)
#     df['entry_price'] = np.where(df['pos_change'] != 0, np.where(df['pos'] == 1, df['contract_spread'], np.where(df['pos'] == -1, df['extend_spread'],0)), 0)
#     df['entry_price'].fillna(method='ffill', inplace=True)
#
#     df['pnl'] = np.where(df['pos_change'] != 0, (
#         np.where(df['pos'].shift(1) == 1, (df['contract_spread'] - df['entry_price'].shift(1)) * 0.004,
#                  np.where(df['pos'].shift(1) == -1, (df['extend_spread'] - df['entry_price'].shift(1)) * 0.004, 0))), 0)
#     df['trade_counts'] = np.where(df['pnl'] != 0, 1, 0)
#     df['cumulative_trade_counts'] = df['trade_counts'].cumsum()
#     df['cumu'] = df['pnl'].cumsum()
#
#
#     annual_return = round(df['pnl'].mean() * 365, 2)
#
#     print(df.head(2000))
#     # print(df)
#
#     # return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])


def base():

    df['ask_spread'] = df['Bybit_BTCUSDC_Ask'] - df['Binance_BTCTUSD_Ask']
    df['bid_spread'] = df['Bybit_BTCUSDC_Bid'] - df['Binance_BTCTUSD_Bid']

    df['pos'] = 0
    df.loc[df['ask_spread'] > 0, 'pos'] = -1
    df.loc[df['ask_spread'] <= 0, 'pos'] = 1

    df['pos_change'] = df['pos'].diff()

    df['entry_price'] = np.nan
    df.loc[(df['pos'] == -1) & (df['pos_change'] != 0), 'entry_price'] = df['ask_spread']
    df.loc[(df['pos'] == 1) & (df['pos_change'] != 0), 'entry_price'] = df['bid_spread']
    df['entry_price'].fillna(method='ffill', inplace=True)

    df['pnl'] = np.where(df['pos_change'] != 0, (df['entry_price'].shift(1) - df['entry_price']) * df['pos'], 0)
    df['cumu'] = df['pnl'].cumsum()


    print(df)
    # print(df)

    # return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])

###### Testing ######
# x= 10
# y = 0
#
# base(x, y)
# base()

# time.sleep(1234)

###### opt zone ######
# ma = np.arange(5, 60, 1)
# z = np.arange(0, 2, 0.1)
#
# result = pd.DataFrame(columns=['x', 'y', 'annual_return'])
#
# for x in ma:
#     for y in z:
#         result = result.append(base(x,y), ignore_index=True)
#
# result = result.sort_values(by='annual_return', ascending=False)
#
# print(result)
#
# table = result.pivot_table(index='x', columns='y', values='annual_return')
# sns.heatmap(table, annot=True, fmt='g', cmap='Greens')
# plt.show()
#
# ###### backtest ######
# x=45
# y=0
# base(x,y)
base()
#
fig = px.line(df, x='timestamp', y=['cumu'], title='Strategy')
fig.show()


###### MA Plot ######



# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['diff'], mode='lines', name='diff'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ma'], mode='lines', name='ma'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['+b'], mode='lines', name='+b'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['-b'], mode='lines', name='-b'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ask_spread'], mode='lines', name='ask_spread'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['bid_spread'], mode='lines', name='bid_spread'))


# Customize the chart appearance
fig.update_layout(
    title='Price Difference, Moving Average, and Bollinger Bands',
    xaxis_title='Timestamp',
    yaxis_title='Value'
)

# Display the chart
fig.show()

