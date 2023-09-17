import datetime
import time
import requests
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
    if float(i['price24hPcnt']) > 0.1:
        up.append(i['symbol'])
    elif float(i['price24hPcnt']) < -0.1:
        down.append(i['symbol'])

print(up)
print(down)
# time.sleep(6666)
# symbol = 'BSVUSDT'
category = 'linear'
interval_map = {
    1: ('1min', '1'),
    3: ('3min', '3'),
    5: ('5min', '5'),
    15: ('15min', '15'),
    30: ('30min', '30'),
    60: ('1h', '60'),
    240: ('4h', '240'),
    360: ('6h', '360'),
    720: ('12h', '720'),
    1440: ('1d', 'D')
}
interval = 60

# data = bybit_request.get_kline(category=category, symbol=symbol, interval=interval)
# print(data)
# time.sleep(1234)

def fetch_all_data(symbol):
    oi_interval, kline_interval = interval_map[interval]

    oi = bybit_request.get_open_interest(category, symbol, limit=200, interval_time=oi_interval)
    oi_list = oi['list']
    funding_rate = bybit_request.get_funding_rate_history(category, symbol)
    response_list = funding_rate['list']
    price_data = bybit_request.get_kline(category=category, symbol=symbol, interval=kline_interval)
    price_data_list = price_data['list']
    # print(oi)
    # print(funding_rate)
    # print(price_data_list)

    df1 = pd.DataFrame(oi_list)
    df1 = df1[['timestamp', 'openInterest']]
    df1['timestamp'] = pd.to_datetime(df1['timestamp'].astype(float), unit='ms')
    df1['openInterest'] = df1['openInterest'].astype(float).astype(int)

    df2 = pd.DataFrame(response_list)
    df2 = df2[['fundingRateTimestamp', 'fundingRate']]
    df2['fundingRateTimestamp'] = pd.to_datetime(df2['fundingRateTimestamp'].astype(float), unit='ms')
    df2['adj_funding_rate'] = df2['fundingRate'].astype(float)-0.0001

    df3 = pd.DataFrame(price_data_list, columns=['startTime', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume', 'turnover'])
    # df3 = df3[['startTime', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume', 'turnover']]
    df3['startTime'] = pd.to_datetime(df3['startTime'].astype(float), unit='ms')
    df3['closePrice'] = df3['closePrice'].astype(float)
    df3.rename(columns={'startTime':'timestamp'}, inplace=True)

    df1 = pd.merge(df1, df3[['timestamp', 'closePrice']], on='timestamp', how='left')

    # Reverse the order of the rows
    df1 = df1.iloc[::-1].reset_index(drop=True)
    df2 = df2.iloc[::-1].reset_index(drop=True)
    df3 = df3.iloc[::-1].reset_index(drop=True)

    timestamp = datetime.datetime.now()
    formated_timestamp = timestamp.strftime('%Hh%Mm%Ss')

    with pd.ExcelWriter(f'{symbol}_{interval}min_{formated_timestamp}.xlsx', engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='OI', index=False)
        df2.to_excel(writer, sheet_name='Funding Rate', index=False)
        df3.to_excel(writer, sheet_name='Price Data', index=False)


def trading_history(category, symbol):
    url = 'https://api.bybit.com/v5/market/recent-trade'
    param = {
        'category': category,
        'symbol' : symbol
    }
    response = requests.get(url, params=param)
    response = response.json()
    data = response['result']['list']
    # pprint(data)

    df = pd.DataFrame(data)

    df['time'] = pd.to_datetime(df['time'].astype(float), unit='ms')
    now = pd.Timestamp.now(tz='UTC')
    five_mins_ago = now - pd.Timedelta(minutes=5)

    # Ensure both are in the same format before comparison
    df = df[df['time'].dt.tz_localize('UTC') > five_mins_ago]

    total_volume = 0.0
    buy_volume = 0.0
    for i in df.to_dict('records'):
        size = float(i['size'])
        total_volume += abs(size)
        if i['side'] == 'Buy':
            buy_volume += size

    buy_ratio = round((buy_volume / total_volume) * 100, 2) if total_volume else 0
    print(f"{symbol} Buy volume ratio: {buy_ratio}%")

    return buy_ratio


# print(df1)
# print(df2)
# while True:
for symbol in up:
    fetch_all_data(symbol)
    buy_ratio = trading_history(category=category, symbol=symbol)
for symbol in down:
    fetch_all_data(symbol)
    buy_ratio = trading_history(category=category, symbol=symbol)


# price drop + oi increase + funding rate < -0.01 : in
# oi < oi ma : out
