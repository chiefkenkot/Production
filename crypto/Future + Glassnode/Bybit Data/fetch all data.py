import datetime

import pandas as pd

from CEX_Request_V3 import ByBitRequest
import pal
from pprint import pprint

# fetch 24hr change, if > 10%, go through all data mining
# if have USDT perp > fetch data; if not, pass

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

bybit_key = pal.bybit_key
bybit_secret = pal.bybit_secret


bybit_request = ByBitRequest(bybit_key, bybit_secret)

all_ticker = bybit_request.get_tickers('linear')['result']['list']

# pprint(all_ticker)

up = []
down = []

for i in all_ticker:
    if i['price24hPcnt'] > '0.1':
        up.append(i['symbol'])
    if i['price24hPcnt'] < '-0.1':
        down.append(i['symbol'])

print(up)
print(down)
symbol = 'ARKUSDT'
category = 'linear'

oi = bybit_request.get_open_interest(category, symbol, limit=200, interval_time='5min')
oi_list = oi['list']
funding_rate = bybit_request.get_funding_rate_history(category, symbol)
response_list = funding_rate['list']
print(oi)
print(funding_rate)

df1 = pd.DataFrame(oi_list)
df1 = df1[['timestamp', 'openInterest']]
df1['timestamp'] = pd.to_datetime(df1['timestamp'].astype(float), unit='ms')

df2 = pd.DataFrame(response_list)
df2 = df2[['fundingRateTimestamp', 'fundingRate']]
df2['fundingRateTimestamp'] = pd.to_datetime(df2['fundingRateTimestamp'].astype(float), unit='ms')

with pd.ExcelWriter(f'{symbol}.xlsx', engine='xlsxwriter') as writer:
    df1.to_excel(writer, sheet_name='OI', index=False)
    df2.to_excel(writer, sheet_name='Funding Rate', index=False)

# print(df1)
# print(df2)