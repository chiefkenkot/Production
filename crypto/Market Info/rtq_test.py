import time
from ByBitRequest import ByBitRequest
import json
import uuid
import pal
from pprint import pprint


by_bit_api_key = pal.api_key
by_bit_secret_key = pal.api_secret
by_bit_url = "https://api.bybit.com"
by_recv_window = str(5000)
by_bit_request = ByBitRequest()
by_bit_request.set_up(by_bit_api_key, by_bit_secret_key, by_recv_window, by_bit_url)

# Get Wallet Balance


def get_wallet_balance():
    response = by_bit_request.get_wallet_balance("SPOT")
    wallet_balance_json_obj = json.loads(response)
    result_obj = wallet_balance_json_obj["result"]
    list_array_obj = result_obj["list"]

    for list_item in list_array_obj:
        wallet_balance_position = []
        coin_array_obj = list_item["coin"]
        account_type = list_item["accountType"]
        for coin_item in coin_array_obj:
            position = {}
            coin_token = coin_item["coin"]
            free_value = coin_item["free"]
            if free_value > '0.15':
                position.update({coin_token: free_value})
                wallet_balance_position.append(position)
            # else:
            #     print(coin_token + 'has no position')
        # print(wallet_balance_position)
        return wallet_balance_position


wallet_balance_position = get_wallet_balance()
get_wallet_balance()

# print(wallet_balance_position)

########## testing ############
# response = by_bit_request.get_wallet_balance("SPOT")
# wallet_balance_json_obj = json.loads(response)
# result_obj = wallet_balance_json_obj["result"]
# list_array_obj = result_obj["list"]
#
# # pprint(list_array_obj)
#
# for list_item in list_array_obj:
#     wallet_balance_position = []
#     coin_array_obj = list_item["coin"]
#     account_type = list_item["accountType"]
#     for coin_item in coin_array_obj:
#         position = {}
#         coin_token = coin_item["coin"]
#         free_value = coin_item["free"]
#         bids_bybit = test3.rtq(coin_token)
#         position_value = str(bids_bybit)*free_value
#         print(position_value)





# print(wallet_balance_position)
# symbols = [list(d.keys())[0] for d in wallet_balance_position]
# print(symbols)
#
# # ['ARB', 'C98', 'MATIC', 'OKSE', 'USDC', 'USDT']
#
# time.sleep(1234)

# [{'ARB': '0.00192'}, {'C98': '7.73226'}, {'MATIC': '0.00461'}, {'OKSE': '0.00291'}, {'USDC': '0.0002'}, {'USDT': '99.955001445'}]


# buy_list_2 = ['ARBUSDT', 'MATICUSDT']


# def compare_holding():
#     for pair in wallet_balance_position:
#         coin = f'{list(pair.keys())[0]}USDT' # extract the coin key from the dictionary
#         balance = list(pair.values())[0] # extract the coin key from the dictionary
#         if coin in buy_list_2:
#             #check the 24hr
#             #send sell order if needed
#             print(coin + " is in buy list")
#         else:
#             print(coin + " is not in buy list") #send buy order



# ARBUSDT is in buy list
# C98USDT is not in buy list
# MATICUSDT is in buy list
# OKSEUSDT is not in buy list
# USDCUSDT is not in buy list
# USDTUSDT is not in buy list


# compare_holding()


# time.sleep(1234)

# coin1, balance1 = compare_holding()

# print(coin1)





    # wallet_balance_account.update({account_type: wallet_balance_position})
    # wallet_balance_account.update(wallet_balance_position)

# print(wallet_balance_account)
# print(wallet_balance_position)



# Get Postion list

# loop tickets? GET /v5/market/tickers
# GET /v5/market/tickers?category=spot&symbol=BTCUSDT
# response = by_bit_request.get_market_price("spot", "USDT")
# print("controller get_market_price: " + response)

# POST /v5/order/create
# category = "spot"
# symbol = "ARBUSDT"
# side = "Buy"
# order_type = "Limit"
# qty = "50"
# price = "1"
# time_in_force = "GTC"
# order_link_id = uuid.uuid4().hex
# is_leverage = 0
# order_filter = "Order"
# response = by_bit_request.place_market_order(category, side, symbol, order_type, price, qty, time_in_force,
#                                              order_link_id, is_leverage, order_filter)
# print("controller place_market_order: " + response)