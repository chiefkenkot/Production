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

df = pd.read_csv('BTC_Deribit-Binance-Bitget - 15 Sec.csv')

# df = df[['timestamp','Binance_BTCTUSD', 'Bybit_BTCUSDT']]
df = df[['timestamp', 'Binance_BTCTUSD_bid', 'Binance_BTCTUSD_ask', 'Bitget_BTCUSDTUMCBL_bid', 'Bitget_BTCUSDTUMCBL_ask']]


###### Fee Version ######
# def base():
#     df['diff'] = df['Bitget_BTCUSDTUMCBL_ask'] - df['Binance_BTCTUSD_ask']
#     # df['diff'] = df['Binance_BTCTUSD'] - df['Deribit_BTCPERPETUAL']
#     # df['diff'] = df['Bybit_BTCUSDT'] - df['Deribit_BTCPERPETUAL']
#     df['adj_diff'] = df['diff']*0.003
#     df['fee'] = df['Bitget_BTCUSDTUMCBL_ask']*0.003*0.00002
#
#     # Calculate the upper and lower bounds
#     # df['+b'] = df['adj_diff'] + df['fee']
#     # df['-b'] = df['adj_diff'] - df['fee']
#
#     # df['pos'] = np.where((df['diff'] > (df['ma'] + df['fee']), (np.where(df['z'] > y , -1)), (np.where(df['diff'] < (df['ma'] - df['fee']), (np.where(df['z'] < -y , 1, 0))))
#     # df['pos'] = np.where(df['diff'] > df['+b'], np.where(df['z'] > y, -1), (np.where(df['diff'] < df['-b'], np.where(df['z'] < -y, 1, 0), 0)))
#     df['pos'] = np.where((df['adj_diff'] - df['fee']) > 0, 1, 0)
#
#     # Calculate the change in position
#     df['pos_change'] = df['pos'].diff()
#
#     # Calculate the entry price
#     df['entry_price'] = np.where(df['pos_change'] != 0, df['adj_diff'], np.nan)
#     df['entry_price'].fillna(method='ffill', inplace=True)
#
#     # Calculate the Profit or Loss (PnL) for each trade
#     df['pnl'] = np.where(df['pos_change'] != 0, df['pos'] * (df['adj_diff'] - df['entry_price']) - df['fee'], 0)
#     df['trade_counts'] = np.where(df['pnl'] != 0, 1, 0)
#
#     # Calculate cumulative trade counts and cumulative PnL
#     df['cumulative_trade_counts'] = df['trade_counts'].cumsum()
#     df['cumu'] = df['pnl'].cumsum()
#
#     # Print the first 2000 rows of the DataFrame for checking the intermediate results
#     print(df)
#
#     # Calculate and return the annual return
#     annual_return = round(df['pnl'].mean() * 365, 2)
#     return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])


##### BBAND Version ######
def base(x, y):
    # df['diff'] = df['Bitget_BTCUSDTUMCBL_ask'] - df['Binance_BTCTUSD_ask']
    df['diff'] = df['Binance_BTCTUSD_bid'] - df['Bitget_BTCUSDTUMCBL_bid']
    # df['diff'] = df['Binance_BTCTUSD'] - df['Deribit_BTCPERPETUAL']
    df['adj_diff'] = df['diff'] * 0.001
    df['ma'] = df['adj_diff'].rolling(x).mean()
    df['sd'] = df['adj_diff'].rolling(x).std()
    df['z'] = (df['adj_diff'] - df['ma']) / df['sd']


    # Calculate the upper and lower bounds
    df['+b'] = df['ma'] + df['sd'] * y
    df['-b'] = df['ma'] - df['sd'] * y

    # df['pnl'] = np.where(df['pos_change'] != 0, df['pos_change'] * (df['diff'] - df['entry_price']), 0)
    df['fee'] = df['Bitget_BTCUSDTUMCBL_ask'] * 0.001 * 0.0004
    # df['fee'] = df['Deribit_BTCPERPETUAL']*0.004*0.00006
    # df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))
    # df['pos'] = np.where(df['adj_diff'] - df['fee'] > 0, np.where(df['z'] > y, -1, np.where(df['z'] < -y, 0),0), 0)
    # df['pos'] = np.where(df['adj_diff'] - df['fee'] > 0, np.where(df['adj_diff'] > df['+b'], -1, np.where(df['adj_diff'] < df['-b'], 0, -1)), 0)
    # df['pos'] = np.where(df['adj_diff'] - df['fee'] > 0, -1, 0)
    # Initialize 'pos' column with NaN
    df['pos'] = np.nan

    # Set position to -1 where adj_diff > +b
    df.loc[df['adj_diff'] > df['+b'], 'pos'] = -1

    # Set position to 1 where adj_diff < -b
    df.loc[df['adj_diff'] < df['-b'], 'pos'] = 0

    # Forward fill positions to maintain position when within bounds
    df['pos'].fillna(method='ffill', inplace=True)

    # Fill any remaining NaN values with 0 (this will be the case for the initial values where we don't have enough data to calculate the bounds)
    df['pos'].fillna(0, inplace=True)
    df['pos_change'] = df['pos'].diff()

    df['entry_price'] = np.where(df['pos_change'] != 0, df['adj_diff'], np.nan)
    df['entry_price'].fillna(method='ffill', inplace=True)


    df['pnl'] = np.where(df['pos_change'] != 0, ((abs(df['pos_change']) * (df['adj_diff'] - df['entry_price'].shift(1))) * 0.003 - abs(df['fee']*df['pos_change'])), 0)
    df['trade_counts'] = np.where(df['pnl'] != 0, 1, 0)
    df['cumulative_trade_counts'] = df['trade_counts'].cumsum()
    df['cumu'] = df['pnl'].cumsum()

    # print(df.head(2000))
    print(df.tail(100))

    annual_return = round(df['pnl'].mean() * 365, 2)

    # print(df.tail(20))

    return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])

###### Testing ######
# x= 50
# y = 0
#
# base(x, y)
#
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

###### backtest ######
x=50
y=0.6
base(x,y)
# base()
#
fig = px.line(df, x='timestamp', y=['cumu'], title='Strategy')
fig.show()


###### MA Plot ######

fig = go.Figure()

# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['diff'], mode='lines', name='diff'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ma'], mode='lines', name='ma'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['+b'], mode='lines', name='+b'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['-b'], mode='lines', name='-b'))

fig.add_trace(go.Scatter(x=df['timestamp'], y=df['adj_diff'], mode='lines', name='adj_diff'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ma'], mode='lines', name='ma'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['+b'], mode='lines', name='+b'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['-b'], mode='lines', name='-b'))


# Customize the chart appearance
fig.update_layout(
    title='Price Difference, Moving Average, and Bollinger Bands',
    xaxis_title='Timestamp',
    yaxis_title='Value'
)

# Display the chart
fig.show()

