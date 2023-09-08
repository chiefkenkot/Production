
from ByBitRequest import ByBitRequest
import json
import uuid
import pal

by_bit_api_key=pal.bybit_key
by_bit_secret_key=pal.bybit_secret
by_bit_url = "https://api.bybit.com"
by_recv_window = str(5000)
by_bit_request = ByBitRequest()
by_bit_request.set_up(by_bit_api_key,by_bit_secret_key,by_recv_window,by_bit_url)


#POST /v5/order/create
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
    order_filter = "Order")


def bybit_market():
    by_bit_request.place_market_order(
        category="spot",
        symbol="USDCUSDT",
        side="Sell",
        order_type="Market",
        qty="10",
        is_leverage=0,
        order_filter="Order")

bybit_market()


