import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# insert your API key here
API_KEY = '2IXXpwplgCoKrZg3JOJ5jR7TYWq'

# set time to download
since = 1647527400 # 2022 Mar 17
# since = 1669852800 # 2022 Dec 1
until = 1675349103 # 2023 Jan 25

# until = 1669852800 # 2022 Dec 1
# resolution = "1h"
resolution = "1h" # 10m, 1h, 24h, 1w, 1month

res = requests.get("https://api.glassnode.com/v1/metrics/market/price_usd_close",
    params={"a": "APE", "s": since, "u": until, "api_key": API_KEY, "i": resolution})
df_value = pd.read_json(res.text, convert_dates=['t'])

res = requests.get("https://api.glassnode.com/v1/metrics/market/price_usd_close",
    params={"a": "APE", "s": since, "u": until, "api_key": API_KEY, "i": resolution})
df_price = pd.read_json(res.text, convert_dates=['t'])

df = pd.merge(df_value,df_price,how='inner',on='t')
df = df.rename(columns={'v_x':'value','v_y':'price'})


# print(df)
# time.sleep(1234)

# df = pd.read_csv('BTC-USD.csv')
# df = df[['Date','value']]
df['pct_change'] = df['price'].pct_change()

### define a function
def ma_diff(x,y):

    df['ma'] = df['value'].rolling(x).mean()

    df['ma_diff'] = df['value'] / df['ma']

    # for i in range(len(df)):
    #     if (df.loc[i,'value'] / df.loc[i,'ma'] - 1) > y:
    #         df.loc[i, 'pos'] = 1
    #     elif (df.loc[i,'value'] / df.loc[i,'ma'] - 1) < -y:
    #         df.loc[i, 'pos'] = -1
    #     else:
    #         df.loc[i, 'pos'] = 0

    df['pos'] = np.where(df['ma_diff'] > y, 1, np.where(df['ma_diff'] < -y, -1, 0))

    df['pos_t-1'] = df['pos'].shift(1)
    df['pnl'] = df['pos_t-1'] * df['pct_change']
    df['cumu'] = df['pnl'].cumsum()

    ### buy & hold cumu
    df['bnh_pnl'] = df['pct_change']
    df.loc[0:x-1,'bnh_pnl'] = 0
    df['bnh_cumu'] = df['bnh_pnl'].cumsum()

    # sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24) ## 1hr
    sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24*6) ## 10m
    sharpe = round(sharpe,2)

    ### buy and hold sharpe
    # bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24) ## 1hr
    bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24*6) ## 10m
    bnh_sharpe = round(bnh_sharpe,2)

    # annual_return = round(df['pnl'].mean() * (365*24), 2) ## 1hr
    annual_return = round(df['pnl'].mean() * (365*24*6), 2) ## 10m
    df['dd'] = df['cumu'].cummax() - df['cumu']
    mdd = round(df['dd'].max(),3)
    calmar = round(annual_return / mdd,2)

    # print(df)
    # print(x, y, 'sharpe', sharpe, 'bnh_sharpe', bnh_sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)
    print(x, y, 'sharpe', sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)

def bband(x,y):

    df['ma'] = df['value'].rolling(x).mean()
    df['sd'] = df['value'].rolling(x).std()
    df['z'] = (df['value'] - df['ma']) / df['sd']

    # for i in range(len(df)):
    #     if df.loc[i, 'z'] > y:
    #         df.loc[i, 'pos'] = 1
    #     elif df.loc[i, 'z'] < -y:
    #         df.loc[i, 'pos'] = -1
    #     else:
    #         df.loc[i, 'pos'] = 0

    df['pos'] = np.where(df['z'] > y, 1, np.where(df['z'] < -y, -1, 0))

    df['pos_t-1'] = df['pos'].shift(1)
    df['trade'] = abs(df['pos_t-1'] - df['pos'])
    df['cost'] = df['trade'] *0.05/100
    df['pnl'] = df['pos_t-1'] * df['pct_change'] - df['cost']
    df['cumu'] = df['pnl'].cumsum()

    ### buy & hold cumu
    df['bnh_pnl'] = df['pct_change']
    df.loc[0:x-1,'bnh_pnl'] = 0
    df['bnh_cumu'] = df['bnh_pnl'].cumsum()

    sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24) ## 1hr
    # sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24*6) ## 10m
    sharpe = round(sharpe,2)

    ### buy and hold sharpe
    bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24) ## 1hr
    # bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24*6) ## 10m
    bnh_sharpe = round(bnh_sharpe,2)

    annual_return = round(df['pnl'].mean() * (365*24), 2) ## 1hr
    # annual_return = round(df['pnl'].mean() * (365*24*6), 2) ## 10m
    df['dd'] = df['cumu'].cummax() - df['cumu']
    mdd = round(df['dd'].max(),3)
    calmar = round(annual_return / mdd,2)

    # print(df)
    # print(x, y, 'sharpe', sharpe, 'bnh_sharpe', bnh_sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)
    print(x, y, 'sharpe', sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)

    return pd.Series([x,y,sharpe],index=['x','y','sharpe'])


def bband_reversion(x,y):

    df['ma'] = df['value'].rolling(x).mean()
    df['sd'] = df['value'].rolling(x).std()
    df['z'] = (df['value'] - df['ma']) / df['sd']

    # for i in range(len(df)):
    #     if df.loc[i, 'z'] > y:
    #         df.loc[i, 'pos'] = 1
    #     elif df.loc[i, 'z'] < -y:
    #         df.loc[i, 'pos'] = -1
    #     else:
    #         df.loc[i, 'pos'] = 0

    df['pos'] = np.where(df['z'] > y, -1, np.where(df['z'] < -y, 1, 0))

    df['pos_t-1'] = df['pos'].shift(1)
    df['trade'] = abs(df['pos_t-1'] - df['pos'])
    df['cost'] = df['trade'] *0.05/100
    df['pnl'] = df['pos_t-1'] * df['pct_change'] - df['cost']
    df['cumu'] = df['pnl'].cumsum()

    ### buy & hold cumu
    df['bnh_pnl'] = df['pct_change']
    df.loc[0:x-1,'bnh_pnl'] = 0
    df['bnh_cumu'] = df['bnh_pnl'].cumsum()

    # sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24) ## 1hr
    sharpe = df['pnl'].mean() / df['pnl'].std() * np.sqrt(365*24*6) ## 10m
    sharpe = round(sharpe,2)

    ### buy and hold sharpe
    # bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24) ## 1hr
    bnh_sharpe = df['bnh_pnl'].mean() / df['bnh_pnl'].std() * np.sqrt(365*24*6) ## 10m
    bnh_sharpe = round(bnh_sharpe,2)

    annual_return = round(df['pnl'].mean() * (365*24), 2) ## 1hr
    # annual_return = round(df['pnl'].mean() * (365*24*6), 2) ## 10m
    df['dd'] = df['cumu'].cummax() - df['cumu']
    mdd = round(df['dd'].max(),3)
    calmar = round(annual_return / mdd,2)

    # print(df)
    # print(x, y, 'sharpe', sharpe, 'bnh_sharpe', bnh_sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)
    print(x, y, 'sharpe', sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)

    return pd.Series([x,y,sharpe],index=['x','y','sharpe'])


# ######### optimization zone ##########

ma_list = np.arange(5,100,5)
# thres_list = np.arange(0.01,0.05,0.01)
thres_list = np.arange(0,3,0.25)

result_df = pd.DataFrame(columns=['x','y','sharpe'])

for x in ma_list:
    for y in thres_list:
        # ma_diff(x, y)
        # result_df = result_df.append(ma_diff(x, y), ignore_index=True)

        bband(x,y)
        result_df = result_df.append(bband(x,y), ignore_index=True)

        # bband_reversion(x, y)
        # result_df = result_df.append(bband_reversion(x,y), ignore_index=True)

result_df = result_df.sort_values(by='sharpe', ascending=False)
print(result_df)

data_table = result_df.pivot(index='x',columns='y',values='sharpe')
sns.heatmap(data_table, annot=True, fmt='g', cmap='Greens')
plt.show()

########## backtesting zone ##########

### parameters
# x = 20
# y = 1.5
# # ma_diff(x,y)
# bband(x,y)
# # bband_reversion(x, y)
# fig = px.line(df, x='t', y=['cumu','dd','bnh_cumu'], title='strategy')
# fig.show()
