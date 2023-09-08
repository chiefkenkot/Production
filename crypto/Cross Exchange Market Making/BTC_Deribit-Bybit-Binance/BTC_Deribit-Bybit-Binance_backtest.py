import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df = pd.read_csv('BTC_Deribit-Bybit-Binance.csv')
# df = df[['timestamp','Binance_BTCTUSD', 'Bybit_BTCUSDT']]
df = df[['timestamp','Binance_BTCTUSD', 'Bybit_BTCUSDT', 'Deribit_BTCPERPETUAL']]


###### Fee Version ######
def base(x, y):
    df['diff'] = df['Binance_BTCTUSD'] - df['Bybit_BTCUSDT']
    # df['diff'] = df['Binance_BTCTUSD'] - df['Deribit_BTCPERPETUAL']
    # df['diff'] = df['Bybit_BTCUSDT'] - df['Deribit_BTCPERPETUAL']
    df['ma'] = df['diff'].rolling(x).mean()
    df['sd'] = df['diff'].rolling(x).std()
    df['z'] = (df['diff'] - df['ma']) / df['sd']

    df['fee'] = df['Bybit_BTCUSDT']*0.004*0.00004
    # df['fee'] = 0
    # df['fee'] = 0
    # Calculate the upper and lower bounds
    df['+b'] = df['ma'] + df['fee']
    df['-b'] = df['ma'] - df['fee']

    # df['pos'] = np.where((df['diff'] > (df['ma'] + df['fee']), (np.where(df['z'] > y , -1)), (np.where(df['diff'] < (df['ma'] - df['fee']), (np.where(df['z'] < -y , 1, 0))))
    # df['pos'] = np.where(df['diff'] > df['+b'], np.where(df['z'] > y, -1), (np.where(df['diff'] < df['-b'], np.where(df['z'] < -y, 1, 0), 0)))
    df['pos'] = np.where(df['diff'] > df['+b']*2, np.where(df['z'] > y, -1, 0),
                         np.where(df['diff'] < df['-b']*2, np.where(df['z'] < -y, 1, 0), 0))
    df['pos_change'] = df['pos'].diff()

    df['entry_price'] = np.where(df['pos_change'] != 0, df['diff'], np.nan)
    df['entry_price'].fillna(method='ffill', inplace=True)

    # df['pnl'] = np.where(df['pos_change'] != 0, df['pos_change'] * (df['diff'] - df['entry_price']), 0)

    # df['fee'] = df['Deribit_BTCPERPETUAL']*0.004*0.0005
    df['pnl'] = np.where(df['pos_change'] != 0, ((df['pos'].shift(1) * (df['diff'] - df['entry_price'].shift(1))) * 0.004 - abs(df['fee']*df['pos_change'])), 0)
    df['trade_counts'] = np.where(df['pnl'] != 0, 1, 0)
    df['cumulative_trade_counts'] = df['trade_counts'].cumsum()
    df['cumu'] = df['pnl'].cumsum()



    annual_return = round(df['pnl'].mean() * 365, 2)

    # print(df.head(2000))

    return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])


##### BBAND Version ######
# def base(x, y):
#     df['diff'] = df['Binance_BTCTUSD'] - df['Bybit_BTCUSDT']
#     # df['diff'] = df['Binance_BTCTUSD'] - df['Deribit_BTCPERPETUAL']
#     df['ma'] = df['diff'].rolling(x).mean()
#     df['sd'] = df['diff'].rolling(x).std()
#     df['z'] = (df['diff'] - df['ma']) / df['sd']
#
#     # Calculate the upper and lower bounds
#     df['+b'] = df['ma'] + df['sd'] * y
#     df['-b'] = df['ma'] - df['sd'] * y
#
#     df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))
#     df['pos_change'] = df['pos'].diff()
#
#     df['entry_price'] = np.where(df['pos_change'] != 0, df['diff'], np.nan)
#     df['entry_price'].fillna(method='ffill', inplace=True)
#
#     # df['pnl'] = np.where(df['pos_change'] != 0, df['pos_change'] * (df['diff'] - df['entry_price']), 0)
#     df['fee'] = df['Bybit_BTCUSDT']*0.004*0.00004
#     # df['fee'] = df['Deribit_BTCPERPETUAL']*0.004*0.00006
#     df['pnl'] = np.where(df['pos_change'] != 0, ((df['pos'].shift(1) * (df['diff'] - df['entry_price'].shift(1))) * 0.004 - abs(df['fee']*df['pos_change'])), 0)
#     df['trade_counts'] = np.where(df['pnl'] != 0, 1, 0)
#     df['cumulative_trade_counts'] = df['trade_counts'].cumsum()
#     df['cumu'] = df['pnl'].cumsum()
#
#     # print(df.head(2000))
#
#     annual_return = round(df['pnl'].mean() * 365, 2)
#
#     # print(df)
#
#     return pd.Series([x, y, annual_return], index=['x', 'y', 'annual_return'])

###### Testing ######
# x= 50
# y = 0
#
# base(x, y)

###### opt zone ######
ma = np.arange(5, 60, 1)
z = np.arange(0, 2, 0.1)

result = pd.DataFrame(columns=['x', 'y', 'annual_return'])

for x in ma:
    for y in z:
        result = result.append(base(x,y), ignore_index=True)

result = result.sort_values(by='annual_return', ascending=False)

print(result)

table = result.pivot_table(index='x', columns='y', values='annual_return')
sns.heatmap(table, annot=True, fmt='g', cmap='Greens')
plt.show()

###### backtest ######
x=50
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

