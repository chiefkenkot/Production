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

###### API Zone ######
exchange = ccxt.bybit({
    'apiKey': pal.api_key,
    'secret': pal.api_secret,
})

markets = exchange.load_markets()

session_auth = usdt_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key=pal.api_key,
    api_secret=pal.api_secret
)

# print('********************************')
symbol = 'APEUSDT'
market = exchange.market(symbol)


###### All Functions ######
def open_long():
    session_auth.place_active_order(
        symbol="APEUSDT",
        side="Buy",
        order_type="Market",
        qty=bet_size,
        # price=5,
        time_in_force="GoodTillCancel",
        reduce_only=False,
        close_on_trigger=False,
        position_idx=0
    )


def settle_long():
    session_auth.place_active_order(
        symbol="APEUSDT",
        side="Sell",
        order_type="Market",
        qty=bet_size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False,
        position_idx=0
    )


def open_short():
    session_auth.place_active_order(
        symbol="APEUSDT",
        side="Sell",
        order_type="Market",
        qty=bet_size,
        # price=5,
        time_in_force="GoodTillCancel",
        reduce_only=False,
        close_on_trigger=False,
        position_idx=0
    )


def settle_short():
    session_auth.place_active_order(
        symbol="APEUSDT",
        side="Buy",
        order_type="Market",
        qty=bet_size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False,
        position_idx=0
    )


def reverse_to_short():
    settle_long()
    time.sleep(1)
    open_short()


def reverse_to_long():
    settle_short()
    time.sleep(1)
    open_long()


### signal ###
def signal(df, x, y):

    df['ma'] = df['close'].rolling(x).mean()
    df['sd'] = df['close'].rolling(x).std()
    df['z'] = (df['close'] - df['ma']) / df['sd']

    df['pos'] = np.where(df['z'] > y, 1, np.where(df['z'] < -y, -1, 0))

    pos = df['pos'].iloc[-1] #read the last row

    # df['dt'] = pd.to_datetime(df['DateTime']/1000, unit='s')

    print(df.tail(10))

    return pos


###### trade ######
def trade(pos):

    ### get account info before trade ###
    net_pos = float(exchange.fetchPositions([symbol])[0]['info']['size'])
    net_pos_side = (exchange.fetchPositions([symbol])[0]['info']['side'])

    ### trade ###
    if pos == 1:
        ### Open Long ###
        if net_pos == 0:
            open_long()
            TG_Pop_Up.tg_pop_long()

        ### -1 to 1 ###
        elif net_pos == bet_size and net_pos_side == 'Sell':
            reverse_to_long()
            TG_Pop_Up.tg_pop_reverse_to_long()

    elif pos == 0:
        ### Settle Long ###
        if net_pos == bet_size and net_pos_side == 'Buy':
            settle_long()
            TG_Pop_Up.tg_pop_settle_long()
        ### Settle Short ###
        elif net_pos == bet_size and net_pos_side == 'Sell':
            settle_short()
            TG_Pop_Up.tg_pop_settle_short()

    elif pos == -1:
        ### Open Short ###
        if net_pos == 0:
            open_short()
            TG_Pop_Up.tg_pop_short()
        ### 1 to -1 ###
        if net_pos == bet_size and net_pos_side == 'Buy':
            reverse_to_short()
            TG_Pop_Up.tg_pop_reverse_to_short()

    time.sleep(1)

    ### get account info after trade ###
    net_pos = float(exchange.fetchPositions([symbol])[0]['info']['size'])
    print('after signal')
    print('net position', net_pos)
    print('nav', datetime.datetime.now(), exchange.fetch_balance()['USDT']['total'])


### param ###
x = 30
y = 0.01
# pos = 0
bet_size = 1 #0.001

while True:

    if datetime.datetime.now().second == 5:

        df = pd.read_csv(r'C:\Users\kenkot\OneDrive\桌面\Python learning\Calvin\Script\Production\Future + Glassnode\APE\data.csv')

        pos = signal(df, x, y)
        print(pos)

        trade(pos)

        time.sleep(555)
