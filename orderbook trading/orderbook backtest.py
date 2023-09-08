import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy.optimize import minimize
import seaborn as sns



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Load your data
df = pd.read_csv('Bybit_USDCUSDT_Orderbook.csv')

###### plot overall graphs ######
# Create a subplot with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add a line for each column except 'best bid' and 'best ask'
for column in df.columns:
    if column not in ['best bid', 'best ask']:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column), secondary_y=False)

# Add 'best ask' on a different y-axis
fig.add_trace(go.Scatter(x=df.index, y=df['best ask'], mode='lines', name='best ask'), secondary_y=True)

# Customize the chart appearance
fig.update_layout(
    title='Best Ask and Other Values Over Time',
    xaxis_title='Index',
    yaxis_title='Value',
)

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# Display the chart
fig.show()
print(df.head(2000))
time.sleep(1234)

###### backtest ######

for n in range(5, 55, 5):

# n = 10
    def ratio(x, y):
        ratio = df[f'ratio {n}']
        best_ask = df['best ask']
        best_bid = df['best bid']
        df['ma'] = ratio.rolling(x).mean()
        df['sd'] = ratio.rolling(x).std()
        df['z'] = (ratio - df['ma']) / df['sd']
        df['price_ma'] = best_ask.rolling(x).mean()
        df['price_ma_change'] = df['price_ma'].diff()
        # df['pos'] = 0
        df['pos'] = np.nan
        df.loc[(best_ask < df['price_ma']) & (ratio > y), 'pos'] = 1
        df.loc[(best_ask > df['price_ma']) & (ratio > y),'pos'] = 0
        # df.loc[(best_ask < df['price_ma']) & (df['z'] > y), 'pos'] = 1
        # df.loc[(best_ask > df['price_ma']) & (df['z'] > y),'pos'] = 0
        df['pos'].fillna(method='ffill', inplace=True)


        df['pos change'] = df['pos'].diff()
        df['entry'] = np.where(df['pos change'] != 0, best_ask, np.nan)
        df['entry'].fillna(method='ffill', inplace=True)
        df['fee'] = best_ask * 0.00002
        df['pnl'] = np.where((df['pos change'] != 0) & (df['pos change'].notnull()), best_bid - df['entry'].shift(1) - df['fee'], 0)
        df['cumu'] = df['pnl'].cumsum()
        df['trade_count'] = abs(df['pos change']).cumsum()

        # print(df.tail(2000))
        return pd.Series([x, y, df['cumu'].iloc[-1], df['trade_count'].iloc[-1]], index=['x','y', 'cumu', 'trade_count'])


#     def ratio(x, y):
#         ratio = df[f'ratio {n}']
#         best_ask = df['best ask']
#         best_bid = df['best bid']
#         df['ma'] = ratio.rolling(x).mean()
#         df['sd'] = ratio.rolling(x).std()
#         df['z'] = (ratio - df['ma']) / df['sd']
#         df['price_ma'] = best_ask.rolling(x).mean()
#         # df['price_ma_change'] = df['price_ma'].diff()
#         df['pos'] = np.nan
#
#         df.loc[(best_ask < df['price_ma']) & (df['z'] > y), 'pos'] = 1
#         df.loc[(best_ask > df['price_ma']) & (df['z'] > y), 'pos'] = 0
#         df['pos'].fillna(method='ffill', inplace=True)
#
#         def update_positions(df):
#             active_positions = 0
#             positions = []
#             for pos in df['pos']:
#                 if pos == 1:
#                     active_positions += 1
#                 elif pos == 0:
#                     active_positions -= 1
#                 active_positions = max(0, min(10, active_positions))
#                 positions.append(active_positions)
#             return positions
#
#         df['active_positions'] = update_positions(df)
#
#         df['pos change'] = df['pos'].diff()
#         df['entry'] = np.where(df['pos change'] != 0, best_ask, np.nan)
#         df['entry'].fillna(method='ffill', inplace=True)
#         df['fee'] = best_ask * 0.0004*0
#         df['pnl'] = np.where((df['pos change'] != 0) & (df['pos change'].notnull()), best_bid - df['entry'].shift(1) - df['fee'], 0)
#         df['cumu'] = df['pnl'].cumsum()
#         df['trade_count'] = abs(df['pos change']).cumsum()
#
#         # print(df[df['pos'].diff() != 0])
#         print(df.tail(2000))
#         return pd.Series([x, y, df['cumu'].iloc[-1], df['trade_count'].iloc[-1]], index=['x','y', 'cumu', 'trade_count'])


    ###### Opt Zone ######

    ma = np.arange(1500, 3000, 50)
    z_score = np.arange(1, 20, 1)

    result = pd.DataFrame(columns=['cumu', 'x', 'y', 'trade_count'])

    for x in ma:
        for y in z_score:
            result = result.append(ratio(x, y), ignore_index=True)

    result = result.sort_values(by='cumu', ascending=False)
    print(result)

    x = int(result['x'].iloc[0])
    y = result['y'].iloc[0]
    trade_count = result['trade_count'].iloc[0]
    cumu = result['cumu'].iloc[0]

    ###### Ploting ######

    # x = 1800
    # y = 5
    ratio(x, y)

    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x= df.index, y=df['cumu'], mode='lines', name='cumu'))
    fig.add_trace(go.Scatter(x=df.index, y=df[f'ratio {n}'], mode='lines', name='ratio'))

    fig.add_trace(go.Scatter(x=df.index, y=df['best ask'], mode='lines', name='best ask'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df.index, y=df['price_ma'], mode='lines', name='ma'), secondary_y=True)
    fig.update_layout(
        title= f'Orderbook Trading: orderbook depth = {n}, ma = {x}, sd = {y}, trade count = {trade_count}, cumu = {cumu}',
        # title= f'Orderbook Trading: orderbook depth = {n}, ma = {x}, sd = {y}',
        yaxis_title='cumu pnl',
        xaxis_title='index'
    )

    fig.show()

