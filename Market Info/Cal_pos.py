import pandas as pd
import requests

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

symbol = 'BTCUSDT'
interval = '60'

def cal_z_score(symbol):
    ####### Request Data ######
    url = "https://api.bybit.com/v5/market/kline"

    param = {'category':'spot',
             'symbol':symbol,
             'interval':'60',
             'limit':'30'}

    response = requests.get(url, params=param)
    response = response.json()['result']['list']
    # print(response)

    close = [i[4] for i in response]

    close = pd.DataFrame(close, columns=['value'])
    close = close.iloc[::-1].reset_index(drop=True)
    # print(close)

    x = 20

    df = pd.DataFrame(close['value'], columns=['value'])
    df.to_csv('3SD.CSV', index=False)

    df = pd.read_csv('3SD.CSV')

    df['ma'] = df['value'].rolling(x).mean()
    df['sd'] = df['value'].rolling(x).std()
    df['z'] = (df['value'] - df['ma']) / df['sd']

    z_score = round(df['z'].iloc[-1], 2)

    return z_score
