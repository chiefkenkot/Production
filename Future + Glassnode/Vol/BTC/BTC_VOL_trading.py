import datetime
import json

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
API_KEY = '2OxypotoPzj1q7frVlYSvtudiiN'

# set time to download
# since = 1647527400 # 2022 Mar 17
since = 1589932800 # 2020 May 20
# since = 1669852800 # 2022 Dec 1
# until = 1675349103 # 2023 Jan 25

# until = 1669852800 # 2022 Dec 1
# resolution = "1h"
resolution = "24h" # 1 week, 2 weeks, 1 month, 3 months, 6 months, and 1 year

res = requests.get("https://api.glassnode.com/v1/metrics/market/realized_volatility_all",
    params={"a": "BTC", "s": since, "api_key": API_KEY, "i": resolution})
df_value = pd.read_json(res.text, convert_dates=['t'])


df_value= df_value['o']

df_value = df_value.apply(lambda x: x['3m'])

df = pd.DataFrame(df_value)

df['value'] = df['o']


# res = requests.get("https://api.glassnode.com/v1/metrics/market/price_usd_close",
#     params={"a": "APE", "s": since, "u": until, "api_key": API_KEY, "i": resolution})
# df_price = pd.read_json(res.text, convert_dates=['t'])

# df = pd.merge(df_value,df_price,how='inner',on='t')
# df = df.rename(columns={'v_x':'value','v_y':'price'})


# print(df)
# time.sleep(1234)

# df = pd.read_csv('BTC-USD.csv')
# df = df[['Date','value']]
df['pct_change'] = df['value'].pct_change()

### define a function

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
    pos = df['pos']
    pos2 = pos.iloc[-1]
    value = df['value']
    value2 = round(value.iloc[-1], 2)
    z = df['z']
    z2 = round(z.iloc[-1], 2)

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

    ## buy and hold sharpe
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
    # print(x, y, 'sharpe', sharpe, 'annual_return', annual_return, 'mdd', mdd, 'calmar', calmar)
    # print(pos.tail(10))

    return pos2, value2, z2
    # return pd.Series([x,y,sharpe],index=['x','y','sharpe'])


def tg_pop(pos2, value2, z2):
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    message = f'BTC Vol signal:{pos2}(VOL={value2}, Z-Score={z2})'

    requests.get(base_url + message)



# print(datetime.datetime.now().hour)

while True:
    try:
        now = datetime.datetime.now()
        if now.hour == 11 and now.minute == 45:
            # insert your API key here
            API_KEY = '2OxypotoPzj1q7frVlYSvtudiiN'

            since = 1669852800 # 2022 Dec 1
            resolution = "24h"  # 1 week, 2 weeks, 1 month, 3 months, 6 months, and 1 year

            res = requests.get("https://api.glassnode.com/v1/metrics/market/realized_volatility_all",
                               params={"a": "BTC", "s": since, "api_key": API_KEY, "i": resolution})
            df_value = pd.read_json(res.text, convert_dates=['t'])

            df_value = df_value['o']

            df_value = df_value.apply(lambda x: x['3m'])

            df = pd.DataFrame(df_value)

            df['value'] = df['o']
            df['pct_change'] = df['value'].pct_change()

            x = 39
            y = 0.05
            pos2, value2, z2 = bband(x,y)
            tg_pop(pos2, value2, z2)
            print(df.tail(10))
            time.sleep(60)
        else:
            time.sleep(40)
    except:
        continue



