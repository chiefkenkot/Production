import ccxt
import time
import pandas as pd
import numpy as np
import datetime
from pprint import pprint
import pal
import TG_Pop_Up
from pybit import usdt_perpetual

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

exchange = ccxt.bybit({
    'apiKey': pal.api_key,
    'secret': pal.api_secret,
})

bet_size = 1

symbol = 'APEUSDT'

net_pos = float(exchange.fetchPositions([symbol])[0]['info']['size'])
net_pos_side = (exchange.fetchPositions([symbol])[0]['info']['side'])

if net_pos == bet_size and net_pos_side == 'Sell':
    print('yes')
else:
    print('no')


# elif pos == 1:
#     if net_pos == bet_size and net_pos_side == 'Sell':

# print(net_pos_side)












