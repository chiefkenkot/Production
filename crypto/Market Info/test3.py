import ccxt
import time
import pandas as pd
import numpy as np
import datetime
from pprint import pprint
import pal
from pybit import usdt_perpetual
from pybit import spot
import requests
import rtq_test
from Cal_pos import cal_z_score

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

##### API Zone ######
session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com", api_key=pal.api_key, api_secret=pal.api_secret
)

###### bid-ask reading ######

def rtq(symbol):
    session_unauth.symbol = symbol

    bids_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['bidPrice']
    asks_bybit = session_unauth.best_bid_ask_price(symbol=symbol)['result']['askPrice']

    # print('######')
    # print(symbol)
    # print(bids_bybit)
    # print(asks_bybit)
    return bids_bybit, asks_bybit


###### Wallet Balance ######
rtq_test.get_wallet_balance()
wallet_balance_position = rtq_test.get_wallet_balance()
num_tokens = len(wallet_balance_position)

# print(num_tokens)
# pprint(wallet_balance)
# time.sleep(1234)

# balances = {d["tokenId"]: float(d["free"]) for d in wallet_balance}

# Print the balances in the format "TOKEN: BALANCE"
# for token, balance in balances.items():
#     print(f"{token}: {balance:.2f}")

# usdt_balance = balances.get("USDT", 0)  # get the USDT balance, default to 0 if not found
# print(f"USDT balance: {usdt_balance:.2f}")

# time.sleep(1234)

###### Order ######
def place_marketsell_order(symbol, balance):
    session_unauth.place_active_order(
        symbol=symbol,
        side='Sell',
        type='MARKET',
        qty=round(float(balance)-0.1,1), # need to adjust '-x' if the qty change!
        timeInForce='GTC',
        )


def place_marketbuy_order(symbol):
    session_unauth.place_active_order(
        symbol=symbol,
        side='Buy',
        type='MARKET',
        # qty=round(float(5 / float(ask_bybit)), 2) - 0.1, #need to adjust '-x' if the qty change!
        qty=10, #input usdt amount
        timeInForce='GTC',
     )

###### TG POP BUY ######
def tg_pop_buy(symbol):
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    message = 'Just bought:' + str(symbol)
    requests.get(base_url + message)


# ###### TG POP SELL ######
def tg_pop_sell(symbol):
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    message = 'Just settled:' + str(symbol)
    requests.get(base_url + message)

# ###### TG POP numtoken ######
def tg_pop_numtoken():
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    message = 'num_tokens:' + str(num_tokens)
    requests.get(base_url + message)

# ###### TG POP TP ######
def tg_pop_take_profit(symbol):
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
    message = 'Take Profit:' + str(symbol)
    requests.get(base_url + message)

def symbol_24hPcnt(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    param2 = {'category': 'spot', 'symbol': symbol}
    response2 = requests.get(url, params=param2)
    spot2 = response2.json()['result']['list'][0]['price24hPcnt']
    return spot2

def get_take_profit(symbol):
    # read CSV file into a DataFrame
    df = pd.read_csv('old_data.csv')

    # filter rows for symbol
    symbol_df = df[df['symbol'] == symbol]

    # check value of take_profit column
    take_profit_value = symbol_df.iloc[0]['take_profit']
    return take_profit_value

# time.sleep(1234)

###### Request #######

url = 'https://api.bybit.com/v5/market/tickers'

param = {'category': 'spot'}

# symbol = 'BTCUSDT'
# # url = 'https://api.bybit.com/v5/market/tickers'
# param2 = {'category': 'spot', 'symbol': symbol}
# response2 = requests.get(url, params=param2)
# # spot2 = response2.json()['result']['list'][0]['price24hPcnt']
# spot2 = response2.json()['result']['list']['price24hPcnt']
# pprint(spot2)
# time.sleep(1234)

####### kick off to generate 'old_data.csv' ######
response = requests.get(url, params=param)

spot_list = response.json()['result']['list']


df_new = pd.DataFrame.from_dict(spot_list)
df_new = df_new[['symbol', 'price24hPcnt', 'lastPrice', 'highPrice24h']]
df_new['take_profit'] = np.where(df_new['highPrice24h'].astype(float) * 0.85 < df_new['lastPrice'].astype(float), 1, 0)


####### Extract Data to CSV #######
df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)

exclude_list = ["USDC", "BTC", "DAI", '2S', '3S', '2L', '3L', 'SEOR', 'FAME', 'MNZ', 'DICE', 'PSTAKE', 'RUNE',
                        'DPX', 'XETA', 'TWT', 'GENE', 'MEE', 'GSTS', 'HERO', 'LING', 'ELT', 'LFW']

for exclude_string in exclude_list:
    df_new = pd.DataFrame([item for item in df_new.values if exclude_string not in item[0]], columns=df_new.columns)

df_new.to_csv('old_data.csv', index=False)


####### Shortlisting #######
df_above_13 = df_new[df_new['price24hPcnt'] > '0.13']
symbol_above_13 = list(df_above_13['symbol'])
# print(symbol_above_13)
# print(df_new)

# tokens = ['ACSUSDT', 'QMALLUSDT', 'XETAUSDT']


time.sleep(5)

####### Looping #######
pct_change = 0.13

while True:
    try:
        ###### Request Data ######
        response = requests.get(url, params=param)

        spot_list = response.json()['result']['list']

        df_new = pd.DataFrame.from_dict(spot_list)
        df_new = df_new[['symbol', 'price24hPcnt', 'lastPrice', 'highPrice24h']]
        df_new = df_new.sort_values(by=['price24hPcnt'], ascending=False)
        df_new['take_profit'] = np.where(df_new['highPrice24h'].astype(float) * 0.85 < df_new['lastPrice'].astype(float), 1, 0)

        ###### Filter out USDC / BTC / DAI pair ######
        exclude_list = ["USDC", "BTC", "DAI", '2S', '3S', '2L', '3L', 'SEOR', 'FAME', 'MNZ', 'DICE', 'PSTAKE', 'RUNE',
                        'DPX', 'XETA', 'TWT', 'GENE', 'MEE', 'GSTS', 'HERO', 'LING', 'ELT', 'LFW']

        for exclude_string in exclude_list:
            df_new = pd.DataFrame([item for item in df_new.values if exclude_string not in item[0]], columns=df_new.columns)

        ###### Buy List ######
        df_above_13 = df_new[df_new['price24hPcnt'] > str(pct_change)]
        symbol_above_13 = list(df_above_13['symbol'])
        # print(symbol_above_13)

        df_old = pd.read_csv('old_data.csv')
        df_old = df_old[df_old['price24hPcnt'] > pct_change]
        old_symbol_above_13 = list(df_old['symbol'])
        # print(old_symbol_above_13)

        buy_list = set(symbol_above_13) - set(old_symbol_above_13)
        # print(buy_list)

        # Save the new DataFrame to the CSV file
        df_new.to_csv('old_data.csv', index=False)

        ###### Check How Many / Which Token in Wallet ######
        rtq_test.get_wallet_balance()
        wallet_balance_position = rtq_test.get_wallet_balance()
        num_tokens = len(wallet_balance_position)
        symbol_list = [list(d.keys())[0] for d in wallet_balance_position]
        symbol_list = [symbol + 'USDT' for symbol in symbol_list]

        ###### If holding wallet turns -% > Sell Order ######
        for pair in wallet_balance_position:
            symbol = f'{list(pair.keys())[0]}USDT' # extract the coin key from the dictionary
            balance = list(pair.values())[0] # extract the coin key from the dictionary
            z_score = cal_z_score(symbol)
            print(z_score)
            print(symbol)
            # print(balance)
            if symbol == 'USDTUSDT':
                print('######')
            else:
                pcnt = symbol_24hPcnt(symbol)
                if pcnt < '0':
                    # place_marketsell_order(symbol, balance)
                    # tg_pop_sell(symbol)
                    print('pcnt < 0')
                if z_score >= 1.0:
                    # take_profit_value = get_take_profit(symbol)
                    # if take_profit_value == 1:
                    print(f'{symbol} take_profit_value')
                        # place_marketsell_order(symbol,balance)
                        # tg_pop_take_profit(symbol)
                else:
                    pass

        ###### If Token is not in Buy List > Buy Order ######
        if num_tokens <= 16: # not fully loaded
            for symbol in buy_list:
                # if f"{symbol}USDT" in balances: # check if i already have the token in buy list
                if symbol in symbol_list: # check if i already have the token in buy list
                    print(f"{symbol}: bought")
                    pass
                else:
                    print(f"{symbol}: buy now") # place buy order
                    bids_bybit, asks_bybit = rtq(symbol)  # store the values returned by rtq()
                    # place_marketbuy_order(symbol)
                    # tg_pop_buy(symbol)
                    # tg_pop_numtoken()
        else:
            print('loaded')

        # Wait for 1 minutes before making the next request
        time.sleep(5)

    except:
        continue


