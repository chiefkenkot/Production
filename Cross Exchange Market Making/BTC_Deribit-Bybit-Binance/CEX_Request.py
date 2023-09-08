import json
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import base64

class ByBitRequest:
    def __init__(self) -> None:
        pass

    def set_up(self, api_key, secret_key, recv_windows, url_path):
        self.api_key = api_key
        self.secret_key = secret_key
        self.httpClient = requests.Session()
        self.recv_window = recv_windows
        self.url_path = url_path  # Testnet endpoint

    def gen_signature(self, time_stamp, payload):
        param_str = str(time_stamp) + self.api_key + self.recv_window + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def send_http_rquest(self, end_point, method, payload):
        time_stamp = str(int(time.time() * 10 ** 3))
        signature = self.gen_signature(time_stamp, payload)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }

        if (method == "POST"):
            response = self.httpClient.request(method, self.url_path + end_point, headers=headers, data=payload)
        else:
            response = self.httpClient.request(method, self.url_path + end_point + "?" + payload, headers=headers)

        # print("Status code:", response.status_code)  # Add this line to print the status code
        # print("Response JSON:", response.json())
        # print(end_point + " Elapsed Time : " + str(response.elapsed))
        return response

    def get_market_price(self, category, symbol):
        end_point = "/v5/market/orderbook"
        params_fomat = "category={category_value}&symbol={symbol_value}"
        params = params_fomat.format(category_value=category, symbol_value=symbol)
        method = "GET"
        response = self.send_http_rquest(end_point, method, params)
        return response

    def get_wallet_balance(self, account_type, coin=""):
        end_point = "/v5/account/wallet-balance"
        params_fomat = "accountType={accountType_value}&coin={coin_value}"
        if (coin == ""):
            params_fomat = "accountType={accountType_value}"
            params = params_fomat.format(accountType_value=account_type)
        else:
            params = params_fomat.format(accountType_value=account_type, coin_value=coin)

        method = "GET"
        response = self.send_http_rquest(end_point, method, params)
        return response

    def get_open_orders(self, category, symbol=None):
        end_point = "/v5/order/realtime"
        params_format = "category={category}"

        if symbol:
            params_format += "&symbol={symbol}"

        params = params_format.format(category=category, symbol=symbol)

        method = "GET"
        response = self.send_http_rquest(end_point, method, params)

        return response

    def place_limit_order(self, category, side, symbol, order_type, price, qty, time_in_force, order_link_id,
                          is_leverage, order_filter):
        end_point = "/v5/order/create"
        params_format = '{{"symbol":{symbol_value},"orderType":{order_type_value},"side":{side_value},"qty":{qty_value},"price":{price_value},"timeInForce":{time_in_force_value},"category":{category_value},"orderLinkId": "{order_link_id_value}","isLeverage":{is_leverage_value},"orderFilter":"{order_filter_value}"}}'
        params = params_format.format(symbol_value=f'"{symbol}"', order_type_value=f'"{order_type}"',
                                      side_value=f'"{side}"', qty_value=f'"{qty}"', price_value=f'"{price}"',
                                      time_in_force_value=f'"{time_in_force}"', category_value=f'"{category}"',
                                      order_link_id_value=order_link_id, is_leverage_value=is_leverage,
                                      order_filter_value=order_filter)

        print("Request parameters:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        return response

    def place_market_order(self, category, side, symbol, order_type, qty, is_leverage, order_filter):
        end_point = "/v5/order/create"
        params_format = '{{"symbol":{symbol_value},"orderType":{order_type_value},"side":{side_value},"qty":{qty_value},"category":{category_value},"isLeverage":{is_leverage_value},"orderFilter":"{order_filter_value}"}}'
        params = params_format.format(symbol_value=f'"{symbol}"', order_type_value=f'"{order_type}"',
                                      side_value=f'"{side}"', qty_value=f'"{qty}"',
                                      category_value=f'"{category}"', is_leverage_value=is_leverage,
                                      order_filter_value=order_filter)

        print("Request parameters:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        return response

    def cancel_all_orders(self, category, symbol=None, base_coin=None, settle_coin=None, order_filter=None):
        end_point = "/v5/order/cancel-all"
        params_format = '{{"category":{category_value},"symbol":{symbol_value},"baseCoin":{base_coin_value},"settleCoin":{settle_coin_value},"orderFilter":{order_filter_value}}}'
        params = params_format.format(category_value=f'"{category}"',
                                      symbol_value=f'"{symbol}"' if symbol else "null",
                                      base_coin_value=f'"{base_coin}"' if base_coin else "null",
                                      settle_coin_value=f'"{settle_coin}"' if settle_coin else "null",
                                      order_filter_value=f'"{order_filter}"' if order_filter else "null")

        print("Request parameters:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        return response

    def cancel_order(self, category, symbol, order_id=None, order_link_id=None, order_filter=None):
        end_point = "/v5/order/cancel"
        params_format = '{{"category":{category_value},"symbol":{symbol_value},"orderId":{order_id_value},"orderLinkId":{order_link_id_value},"orderFilter":{order_filter_value}}}'
        params = params_format.format(category_value=f'"{category}"', symbol_value=f'"{symbol}"',
                                      order_id_value=f'"{order_id}"' if order_id else "null",
                                      order_link_id_value=f'"{order_link_id}"' if order_link_id else "null",
                                      order_filter_value=f'"{order_filter}"' if order_filter else "null")

        print("Request parameters:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        return response



    def get_position_info(self, category, symbol=None, baseCoin=None, settleCoin=None, limit=20, cursor=None):
        end_point = "/v5/position/list"
        params = {
            "category": category,
        }

        if symbol is not None:
            params["symbol"] = symbol

        if baseCoin is not None:
            params["baseCoin"] = baseCoin

        if settleCoin is not None:
            params["settleCoin"] = settleCoin

        if limit != 20:
            params["limit"] = limit

        if cursor is not None:
            params["cursor"] = cursor

        params_str = urlencode(params)
        # print("Request parameters:", params_str)  # Add this line to print the request parameters

        method = "GET"
        response = self.send_http_rquest(end_point, method, params_str)
        return response



class BinanceRequest:
    def __init__(self, binance_api_key, binance_secret_key):
        self.api_key = binance_api_key
        self.secret_key = binance_secret_key
        self.base_url = 'https://api.binance.com'

    def get_signed_params(self, params):
        query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return query_string + '&signature=' + signature

    def place_order(self, symbol, side, order_type, quantity, price=None, time_in_force='GTC'):
        endpoint = '/api/v3/order'

        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'timestamp': int(time.time() * 1000),
        }

        if price:
            params['price'] = price

        if order_type == 'LIMIT':
            params['timeInForce'] = time_in_force

        signed_params = self.get_signed_params(params)

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        response = requests.post(f'{self.base_url}{endpoint}?{signed_params}', headers=headers)
        return response.json()


    def get_account_info(self, recv_window=None):
        endpoint = '/api/v3/account'

        params = {
            'timestamp': int(time.time() * 1000),
        }

        if recv_window:
            params['recvWindow'] = recv_window

        signed_params = self.get_signed_params(params)

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        response = requests.get(f'{self.base_url}{endpoint}?{signed_params}', headers=headers)
        return response.json()


class Bitget_Request:
    def __init__(self):
        pass

    def set_up(self, api_key, api_secret):
        self.api_key = api_key
        self.secret_key = api_secret
        self.httpClient = requests.Session()
        self.base_url = 'https://api.bitget.com'

    def get_timestamp(self):
        return int(time.time() * 1000)

    def sign(self, message):
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def pre_hash(self, timestamp, method, request_path, body):
        return str(timestamp) + str.upper(method) + request_path + body

    def parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'

        return url[0:-1]

    # Add your methods here, following the structure of the ByBitRequest class.
    # For example:

    def get_account_info(self, symbol, margin_coin):
        end_point = "/api/mix/v1/account/account"
        params = {
            "symbol": symbol,
            "marginCoin": margin_coin
        }

        params_str = self.parse_params_to_str(params)

        timestamp = self.get_timestamp()
        body = ""
        request_path = end_point + params_str
        signature = self.sign(self.pre_hash(timestamp, "GET", request_path, body))

        headers = {
            "BGA-ACCESS-KEY": self.api_key,
            "BGA-ACCESS-SIGN": signature,
            "BGA-ACCESS-TIMESTAMP": str(timestamp),
            "Content-Type": "application/json"
        }

        response = self.httpClient.request("GET", self.base_url + request_path, headers=headers)
        return response


    def place_limit_order(self, symbol, margin_coin, size, side, order_type, price=None, time_in_force_value=None,
                          client_oid=None, reduce_only=False, preset_take_profit_price=None,
                          preset_stop_loss_price=None):
        end_point = "/api/mix/v1/order/placeOrder"

        data = {
            "symbol": symbol,
            "marginCoin": margin_coin,
            "size": size,
            "side": side,
            "orderType": order_type,
            "reduceOnly": reduce_only
        }

        if price is not None:
            data["price"] = price

        if time_in_force_value is not None:
            data["timeInForceValue"] = time_in_force_value

        if client_oid is not None:
            data["clientOid"] = client_oid

        if preset_take_profit_price is not None:
            data["presetTakeProfitPrice"] = preset_take_profit_price

        if preset_stop_loss_price is not None:
            data["presetStopLossPrice"] = preset_stop_loss_price

        timestamp = self.get_timestamp()
        body = json.dumps(data)
        request_path = end_point
        signature = self.sign(self.pre_hash(timestamp, "POST", request_path, body))

        headers = {
            "BGA-ACCESS-KEY": self.api_key,
            "BGA-ACCESS-SIGN": signature,
            "BGA-ACCESS-TIMESTAMP": str(timestamp),
            "Content-Type": "application/json"
        }

        response = self.httpClient.request("POST", self.base_url + request_path, headers=headers, data=body)
        return response


    def get_open_orders(self, symbol):
        end_point = "/api/mix/v1/order/current"

        params = {
            "symbol": symbol
        }

        timestamp = self.get_timestamp()
        request_path = f"{end_point}?{urlencode(params)}"
        signature = self.sign(self.pre_hash(timestamp, "GET", request_path))

        headers = {
            "BGA-ACCESS-KEY": self.api_key,
            "BGA-ACCESS-SIGN": signature,
            "BGA-ACCESS-TIMESTAMP": str(timestamp),
            "Content-Type": "application/json"
        }

        response = self.httpClient.request("GET", self.base_url + request_path, headers=headers)
        return response
    #demo
    # bitget_request = Bitget_Request(api_key, secret_key)
    # symbol = "BTCUSDT_UMCBL"
    # response = bitget_request.get_open_orders(symbol)
    # print(response)


