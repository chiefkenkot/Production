import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def logic():
    df = pd.read_csv('BTC_Bybit-MEXC_Data.csv')
    df = df[['timestamp','MEXC_BTC/USDT_Ask', 'MEXC_BTC/USDT_Bid', 'Bybit_BTCUSDC_Ask', 'Bybit_BTCUSDC_Bid']]

    df['ask_diff'] = df['Bybit_BTCUSDC_Ask'] - df['MEXC_BTC/USDT_Ask']

    df['pos'] = np.nan
    df.loc[df['ask_diff'] > 0, 'pos'] = -1
    df.loc[df['ask_diff'] <= 0, 'pos'] = 1
    df['pos_change'] = df['pos'].diff()
    df['sum'] = abs(df['pos_change']).cumsum()/2

    # print(df.head(2000))
    print(df)






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
# x=17
# y=0
# base(x,y)
# #
# fig = px.line(df, x='timestamp', y=['cumu'], title='Strategy')
# fig.show()
#
#
# ###### MA Plot ######
#
# fig = go.Figure()
#
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['diff'], mode='lines', name='diff'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['ma'], mode='lines', name='ma'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['+b'], mode='lines', name='+b'))
# fig.add_trace(go.Scatter(x=df['timestamp'], y=df['-b'], mode='lines', name='-b'))
#
# # Customize the chart appearance
# fig.update_layout(
#     title='Price Difference, Moving Average, and Bollinger Bands',
#     xaxis_title='Timestamp',
#     yaxis_title='Value'
# )
#
# # Display the chart
# fig.show()

