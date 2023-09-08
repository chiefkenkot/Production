import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df = pd.read_csv('Binance VS MEXC.csv')
df = df[['timestamp','Binance_BTCTUSD', 'MEXC_BTCUSDT']]

# def base(x,y):
#
#     df['diff'] = df['Binance_BTCTUSD'] - df['MEXC_BTCUSDT']
#     df['ma'] = df['diff'].rolling(x).mean()
#     df['sd'] = df['diff'].rolling(x).std()
#     df['z'] = (df['diff']-df['ma'])/df['sd']
#
#     df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < y, 1, 0))
#     # df['pnl'] = np.where(df['pos'] == df['pos'].shift(1), 0, df['pos'] * df['diff'] * 0.004)
#     df['pos_change'] = df['pos'].diff()
#     df['entry_price'] = np.where(df['pos_change'] != 0, df['diff'], np.nan)
#     df['entry_price'].fillna(method='ffill', inplace=True)
#     df['pnl'] = df['pos_change'] * (df['diff'] - df['entry_price'])
#     df['cumu'] = df['pnl'].cumsum()
#
#     # Calculate the upper and lower bounds
#     df['+b'] = df['ma'] + df['sd'] * y
#     df['-b'] = df['ma'] - df['sd'] * y
#
#     annual_return = round(df['pnl'].mean()*365, 2)
#
#     print(df.head(1000))
#
#     return pd.Series([x,y, annual_return], index=['x', 'y', 'annual_return'])

def base(x, y):
    df['diff'] = df['Binance_BTCTUSD'] - df['MEXC_BTCUSDT']
    df['ma'] = df['diff'].rolling(x).mean()
    df['sd'] = df['diff'].rolling(x).std()
    df['z'] = (df['diff'] - df['ma']) / df['sd']

    df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < y, 1, 0))
    df['pos_change'] = df['pos'].diff()

    df['entry_price'] = np.where(df['pos_change'] != 0, df['diff'], np.nan)
    df['entry_price'].fillna(method='ffill', inplace=True)

    # df['pnl'] = np.where(df['pos_change'] != 0, df['pos_change'] * (df['diff'] - df['entry_price']), 0)
    df['pnl'] = np.where(df['pos_change'] != 0, ((df['pos'].shift(1) * (df['diff'] - df['entry_price'].shift(1))) * 0.004), 0)
    df['cumu'] = df['pnl'].cumsum()

    # Calculate the upper and lower bounds
    df['+b'] = df['ma'] + df['sd'] * y
    df['-b'] = df['ma'] - df['sd'] * y

    annual_return = round(df['pnl'].mean() * 365, 2)

    # print(df.head(2000))

    return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])

# x= 5
# y = 1
#
# base(x, y)

###### opt zone ######
# ma = np.arange(1, 30, 1)
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
x=17
y=0
base(x,y)
#
fig = px.line(df, x='timestamp', y=['cumu'], title='Strategy')
fig.show()


###### MA Plot ######

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['timestamp'], y=df['diff'], mode='lines', name='diff'))
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

