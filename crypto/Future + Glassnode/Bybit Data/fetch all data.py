from CEX_Request_V2 import ByBitRequest
import pal
from pprint import pprint

# fetch 24hr change, if > 10%, go through all data mining
# if have USDT perp > fetch data; if not, pass

bybit_key = pal.bybit_key
bybit_secret = pal.bybit_secret


bybit_request = ByBitRequest(bybit_key, bybit_secret)

all_ticker = bybit_request.get_tickers('linear')['result']['list']

pprint(all_ticker)

up = []
down = []

for i in all_ticker:
    if i['price24hPcnt'] > '0.1':
        up.append(i['symbol'])
    if i['price24hPcnt'] < '-0.1':
        down.append(i['symbol'])

print(up)
print(down)