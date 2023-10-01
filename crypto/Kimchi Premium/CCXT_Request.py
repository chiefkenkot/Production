import ccxt
from pprint import pprint
import time

# print(ccxt.exchanges)
# ['ace', 'alpaca', 'ascendex', 'bequant', 'bigone', 'binance', 'binancecoinm', 'binanceus', 'binanceusdm', 'bingx', 'bit2c', 'bitbank', 'bitbay', 'bitbns', 'bitcoincom', 'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex', 'bitget', 'bithumb', 'bitmart', 'bitmex', 'bitopro', 'bitpanda', 'bitrue', 'bitso', 'bitstamp', 'bitstamp1', 'bittrex', 'bitvavo', 'bkex', 'bl3p', 'blockchaincom', 'btcalpha', 'btcbox', 'btcmarkets', 'btctradeua', 'btcturk', 'bybit', 'cex', 'coinbase', 'coinbaseprime', 'coinbasepro', 'coincheck', 'coinex', 'coinfalcon', 'coinmate', 'coinone', 'coinsph', 'coinspot', 'cryptocom', 'currencycom', 'delta', 'deribit', 'digifinex', 'exmo', 'fmfwio', 'gate', 'gateio', 'gemini', 'hitbtc', 'hitbtc3', 'hollaex', 'huobi', 'huobijp', 'huobipro', 'idex', 'independentreserve', 'indodax', 'kraken', 'krakenfutures', 'kucoin', 'kucoinfutures', 'kuna', 'latoken', 'lbank', 'lbank2', 'luno', 'lykke', 'mercado', 'mexc', 'mexc3', 'ndax', 'novadax', 'oceanex', 'okcoin', 'okex', 'okex5', 'okx', 'paymium', 'phemex', 'poloniex', 'poloniexfutures', 'probit', 'tidex', 'timex', 'tokocrypto', 'upbit', 'wavesexchange', 'wazirx', 'whitebit', 'woo', 'yobit', 'zaif', 'zonda']

# '1m': '1minute',
# '1h': '1hour',
# '1d': '1day',
# '1M': '1month',
# '1y': '1year',

binance = ccxt.binance()  # Instantiate the exchange
upbit = ccxt.upbit()
bybit = ccxt.bybit()
bithumb = ccxt.bithumb()

# Load markets
binance.load_markets()
upbit.load_markets()
bybit.load_markets()
bithumb.load_markets()

binance_set = []
bybit_set = []
upbit_set = []
bithumb_set = []

if binance.has['fetchOHLCV']:
    for symbol in binance.markets:
        # time.sleep(binance.rateLimit / 1000)  # time.sleep wants seconds
        # if 'USDT' in symbol and ':USDT' not in symbol:
            # print(symbol, binance.fetch_ohlcv(symbol, '1h'))  # one day
        binance_set.append(symbol)  # one day
# print(binance_set)

if bybit.has['fetchOHLCV']:
    for symbol in bybit.markets:
        # time.sleep(binance.rateLimit / 1000)  # time.sleep wants seconds
        # if 'USDT' in symbol and ':USDT' not in symbol:
            # print(symbol, binance.fetch_ohlcv(symbol, '1h'))  # one day
        bybit_set.append(symbol)  # one day


if upbit.has['fetchOHLCV']:
    for symbol in upbit.markets:
        # time.sleep(upbit.rateLimit / 1000)  # time.sleep wants seconds
        # if 'USDT' in symbol and ':USDT' not in symbol:
            # print(symbol, binance.fetch_ohlcv(symbol, '1h'))  # one day
        upbit_set.append(symbol)  # one day

# print(upbit_set)

if bithumb.has['fetchOHLCV']:
    for symbol in bithumb.markets:
        # time.sleep(upbit.rateLimit / 1000)  # time.sleep wants seconds
        # if 'USDT' in symbol and ':USDT' not in symbol:
            # print(symbol, binance.fetch_ohlcv(symbol, '1h'))  # one day
        bithumb_set.append(symbol)  # one day


set1 = set(binance_set)
set2 = set(upbit_set)
set3 = set(bybit_set)
set4 = set(bithumb_set)
#
#
common_symbol = set3.intersection(set4)

print(f'total symbol = {len(common_symbol)}')
print(common_symbol)

# bybit vs Upbit
# total symbol = 22
# {'MATIC/BTC', 'DGB/USDT', 'ETC/USDT', 'RVN/USDT', 'XLM/BTC', 'MANA/BTC', 'SOL/BTC', 'BAT/USDT', 'XRP/BTC', 'SAND/BTC', 'ZRX/USDT', 'ALGO/BTC', 'DOGE/USDT', 'ADA/USDT', 'ETH/USDT', 'XRP/USDT', 'TRX/USDT', 'ETH/BTC', 'BCH/USDT', 'DOT/BTC', 'SC/USDT', 'BTC/USDT'}

# binance vs Upbit
# total symbol = 140
# {'NEAR/BTC', 'XEM/BTC', 'STX/BTC', 'GRS/BTC', 'CVC/BTC', 'ETC/BTC', 'ASTR/BTC', 'RVN/BTC', 'SOL/BTC', 'IOST/BTC', 'GAL/BTC', 'NMR/BTC', 'ACM/BTC', 'AVAX/BTC', 'OGN/BTC', 'SNT/BTC', 'MAGIC/BTC', 'ZRX/BTC', 'PLA/BTC', 'HIVE/BTC', 'ATM/BTC', 'NKN/BTC', 'LRC/BTC', 'ZRX/USDT', 'DENT/BTC', 'VET/BTC', 'RAD/BTC', 'STEEM/BTC', 'SNX/BTC', 'STPT/BTC', 'EOS/BTC', 'MANA/BTC', 'IMX/BTC', 'DOT/BTC', 'AGLD/BTC', 'ARK/BTC', 'EGLD/BTC', 'DGB/USDT', 'STMX/BTC', 'API3/BTC', 'GTC/BTC', 'CRV/BTC', 'JST/BTC', 'TUSD/USDT', 'BAR/BTC', 'BTC/USDT', 'YGG/BTC', 'BCH/USDT', 'MTL/BTC', 'COMP/BTC', 'RNDR/BTC', 'ZIL/BTC', 'SEI/BTC', 'XTZ/BTC', 'TRX/BTC', 'TUSD/BTC', 'GLMR/BTC', 'AAVE/BTC', 'LINK/BTC', 'SXP/BTC', 'FIL/BTC', 'UNI/BTC', 'STRAX/BTC', 'GO/BTC', 'ETC/USDT', 'ELF/BTC', 'CYBER/BTC', 'ANKR/BTC', 'POWR/BTC', 'AERGO/BTC', 'ETH/USDT', 'BCH/BTC', 'ALGO/BTC', 'XRP/USDT', 'DAI/BTC', 'BNT/BTC', '1INCH/BTC', 'POLYX/BTC', 'LSK/BTC', 'LINA/BTC', 'MATIC/BTC', 'AUDIO/BTC', 'INJ/BTC', 'APT/BTC', 'RVN/USDT', 'RSR/BTC', 'FLOW/BTC', 'CELO/BTC', 'BAT/USDT', 'OXT/BTC', 'CTSI/BTC', 'DOGE/USDT', 'SAND/BTC', 'JUV/BTC', 'CITY/BTC', 'AXS/BTC', 'ENS/BTC', 'PSG/BTC', 'KAVA/BTC', 'AUCTION/BTC', 'ARPA/BTC', 'STG/BTC', 'MKR/BTC', 'APE/BTC', 'BAT/BTC', 'GLM/BTC', 'SUI/BTC', 'DNT/BTC', 'PROM/BTC', 'ADA/BTC', 'TRX/USDT', 'ARDR/BTC', 'ATOM/BTC', 'OCEAN/BTC', 'SUN/BTC', 'SC/USDT', 'MINA/BTC', 'IOTX/BTC', 'DGB/BTC', 'DOGE/BTC', 'GMT/BTC', 'LOOM/BTC', 'LPT/BTC', 'ADA/USDT', 'ARB/BTC', 'ENJ/BTC', 'CHR/BTC', 'FOR/BTC', 'XRP/BTC', 'GRT/BTC', 'QTUM/BTC', 'WAVES/BTC', 'STORJ/BTC', 'SC/BTC', 'XLM/BTC', 'WAXP/BTC', 'BSV/BTC', 'ETH/BTC', 'RLC/BTC', 'CHZ/BTC'}

# binance vs bithumb
# total symbol = 10
# {'BNB/BTC', 'DOGE/BTC', 'ETH/BTC', 'ENS/BTC', 'XRP/BTC', 'SANTOS/BTC', 'KLAY/BTC', 'PORTO/BTC', 'LAZIO/BTC', 'SOL/BTC'}

# bybit vs bithumb
# total symbol = 3
# {'XRP/BTC', 'SOL/BTC', 'ETH/BTC'}




###### Fetch OHLCV Data of common symbol ######

###### Backtest + Optimise ######

###### Live Trade ######