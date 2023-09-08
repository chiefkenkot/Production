from CEX_Request import ByBitRequest
from CEX_Request import BinanceRequest
import json
import uuid
import pal
import hmac
import hashlib
import time
import urllib
import requests

by_bit_api_key=pal.bybit_key
by_bit_secret_key=pal.bybit_secret
by_bit_url = "https://api.bybit.com"
by_recv_window = str(5000)
by_bit_request = ByBitRequest()
by_bit_request.set_up(by_bit_api_key,by_bit_secret_key,by_recv_window,by_bit_url)

binance_api_key = pal.binance_key
binance_api_secret = pal.binance_secret


###### Order Function ######
def bybit_limit():
    by_bit_request.place_limit_order(
        category = "spot",
        symbol = "BTCUSDT",
        side = "Buy",
        order_type = "Limit",
        qty = "0.004",
        price = "30000",
        time_in_force = "GTC",
        order_link_id = uuid.uuid4().hex,
        is_leverage = 0,
        order_filter = "Order"
    )


def bybit_market_buy():
    by_bit_request.place_market_order(
        category="spot",
        symbol="BTCUSDC",
        side="Buy",
        order_type="Market",
        qty="50", #min 10u
        is_leverage=0,
        order_filter="Order")


def bybit_market_sell():
    by_bit_request.place_market_order(
        category="spot",
        symbol="USDCUSDT",
        side="Sell",
        order_type="Market",
        qty="10", #min 10u
        is_leverage=0,
        order_filter="Order")


def bybit_future_limit():
    order_link_id = uuid.uuid4().hex

    by_bit_request.place_limit_order(
        category = "linear",
        symbol = "USDCUSDT",
        side = "Sell",
        order_type = "Limit",
        qty = "10",
        price = "1.0010",
        time_in_force = "GTC",
        order_link_id = order_link_id,
        is_leverage = 0,
        order_filter = "Order"
    )

    return order_link_id

order_link_id = bybit_future_limit()


def bybit_position(category, bybit_symbol):
    position = bybit_request.get_position_info(category=category, symbol=bybit_symbol)
    position = position.json()
    result = position['result']['list']
    # position_side = result[0]['side']
    # position_size = result[0]['size']
    # position_symbol = result[0]['symbol']

    # return position_symbol, position_side, position_size
    positive_positions = {
        position['symbol']: position['size']
        for position in result
        if float(position['size']) > 0
    }

    return positive_positions

def binance_market_buy():
    api_key = binance_api_key
    secret_key = binance_api_secret

    binance_request = BinanceRequest(api_key, secret_key)

    binance_request.place_order(
        symbol='BTCTUSD',
        side='BUY',  #  'BUY' / 'SELL'
        order_type='MARKET',  # 'LIMIT' / 'MARKET'
        quantity= '50', #min 10u
    )


def binance_market_sell():
    api_key = binance_api_key
    secret_key = binance_api_secret

    binance_request = BinanceRequest(api_key, secret_key)

    binance_request.place_order(
        symbol='BTCTUSD',
        side='SELL',  #  'BUY' / 'SELL'
        order_type='MARKET',  # 'LIMIT' / 'MARKET'
        quantity= '50', #min 10u
    )


