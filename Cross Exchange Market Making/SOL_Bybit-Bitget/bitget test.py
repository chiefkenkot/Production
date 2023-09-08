import requests
import pal

# url = "https://api.bitget.com/api/mix/v1/market/ticker"
# symbol = "BTCUSDT_UMCBL"
#
# querystring = {"symbol": symbol}
#
# response = requests.get(url, params=querystring)
#
# print(response.json())

symbol = 'USDCUSDT'

def fetch_binance_data(symbol):
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    headers = {'X-MBX-APIKEY': pal.binance_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    target_data = None
    for item in data:
        if item['symbol'] == symbol:
            target_data = item
            break

    if target_data is None:
        raise ValueError(f'Symbol {symbol} not found in the response data.')

    ask_price = float(target_data['askPrice'])
    volume = None  # The bookTicker endpoint does not provide 24-hour trading volume.

    return ask_price, volume

ask_price, volume = fetch_binance_data(symbol)

print(ask_price)
print(volume)