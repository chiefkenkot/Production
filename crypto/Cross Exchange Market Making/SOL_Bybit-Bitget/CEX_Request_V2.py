import json
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import base64
import pal
import pytz
from datetime import datetime

class ByBitRequest:

    def __init__(self, api_key: str, secret_key: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.httpClient = requests.Session()
        self.recv_window = '5000'
        self.url_path = 'https://api.bybit.com'

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
        params_format = "accountType={accountType_value}&coin={coin_value}"
        if coin == "":
            params_format = "accountType={accountType_value}"
            params = params_format.format(accountType_value=account_type)
        else:
            params = params_format.format(accountType_value=account_type, coin_value=coin)

        method = "GET"
        response = self.send_http_rquest(end_point, method, params)
        response = response.json()
        coins = response['result']['list'][0]['coin']

        wallet_balance_position = {coin_info['coin']: float(coin_info['free']) for coin_info in coins if
                                   float(coin_info['free']) > 0.05}

        return wallet_balance_position

    def get_open_orders(self, category, symbol=None):
        end_point = "/v5/order/realtime"
        params_format = "category={category}"

        if symbol:
            params_format += "&symbol={symbol}"

        params = params_format.format(category=category, symbol=symbol)

        method = "GET"
        response = self.send_http_rquest(end_point, method, params)

        return response

    def place_limit_order(self, category, side, symbol, order_type, price, qty, time_in_force,
                          is_leverage, order_filter):
        end_point = "/v5/order/create"
        params_format = '{{"symbol":{symbol_value},"orderType":{order_type_value},"side":{side_value},"qty":{qty_value},"price":{price_value},"timeInForce":{time_in_force_value},"category":{category_value},"isLeverage":{is_leverage_value},"orderFilter":"{order_filter_value}"}}'
        params = params_format.format(symbol_value=f'"{symbol}"', order_type_value=f'"{order_type}"',
                                      side_value=f'"{side}"', qty_value=f'"{qty}"', price_value=f'"{price}"',
                                      time_in_force_value=f'"{time_in_force}"', category_value=f'"{category}"',
                                       is_leverage_value=is_leverage,
                                      order_filter_value=order_filter)
        # order_link_id_value = order_link_id,order_link_id ,"orderLinkId": "{order_link_id_value}"
        # print("Request parameters:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        response = response.json()
        orderlink_id = response['result']['orderLinkId']

        return response, orderlink_id

    # Request parameters: {"symbol":"ETHUSDC","orderType":"Limit","side":"Buy","qty":"0.01","price":"1830.8","timeInForce":"GTC","category":"spot","isLeverage":0,"orderFilter":"order"}
    # response = {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1482726557505117696', 'orderLinkId': '1691490779511842'}, 'retExtInfo': {}, 'time': 1691490779524}

    def place_market_order(self, category, side, symbol, order_type, qty, is_leverage, order_filter):
        end_point = "/v5/order/create"
        params_format = '{{"symbol":{symbol_value},"orderType":{order_type_value},"side":{side_value},"qty":{qty_value},"category":{category_value},"isLeverage":{is_leverage_value},"orderFilter":"{order_filter_value}"}}'
        params = params_format.format(symbol_value=f'"{symbol}"', order_type_value=f'"{order_type}"',
                                      side_value=f'"{side}"', qty_value=f'"{qty}"',
                                      category_value=f'"{category}"', is_leverage_value=is_leverage,
                                      order_filter_value=order_filter)

        print("Bybit Order:", params)  # Add this line to print the request parameters

        method = "POST"
        response = self.send_http_rquest(end_point, method, params)
        response = response.json()
        return response

    # if failed: {'retCode': 170229, 'retMsg': 'The sell quantity per order exceeds the estimated maximum sell quantity.', 'result': {}, 'retExtInfo': {}, 'time': 1690741317774}

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
        # Contract only
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
        response = response.json()
        result = response['result']['list']

        side = result[0]['side']
        symbol = result[0]['symbol']
        size = result[0]['size']

        # Creating a new dictionary
        bybit_balance = {
            'side': side,
            'symbol': symbol,
            'size': size
        }

        return bybit_balance, side, symbol, size

    def get_tickers(self, category, symbol=None, baseCoin=None, expDate=None):
        end_point = "/v5/market/tickers"
        params_format = "category={category}"

        if symbol:
            params_format += "&symbol={symbol}"
        if baseCoin:
            params_format += "&baseCoin={baseCoin}"
        if expDate:
            params_format += "&expDate={expDate}"

        params = params_format.format(category=category, symbol=symbol, baseCoin=baseCoin, expDate=expDate)

        method = "GET"
        response = self.send_http_rquest(end_point, method, params)
        response = response.json()
        return response

    def fetch_bybit_data(self, symbol):
        url = 'https://api.bybit.com/v5/market/tickers'
        params = {'category': 'spot'}
        response = requests.get(url, params=params)
        data = response.json()

        # Find the target symbol in the response data
        target_data = None
        for item in data['result']['list']:
            if item['symbol'] == symbol:
                target_data = item
                break

        if target_data is None:
            raise ValueError(f'Symbol {symbol} not found in the response data.')

        ask_price = float(target_data['ask1Price'])
        bid_price = float(target_data['bid1Price'])
        # volume = float(target_data['volume24h'])

        return ask_price, bid_price

    def get_order_history(self, category, symbol=None, baseCoin=None, settleCoin=None, orderId=None,
                          orderLinkId=None, orderFilter=None, orderStatus=None, startTime=None,
                          endTime=None, limit=20, cursor=None):
        end_point = "/v5/order/history"
        params = {"category": category, "limit": limit}

        # Optional parameters
        if symbol:
            params["symbol"] = symbol
        if baseCoin:
            params["baseCoin"] = baseCoin
        if settleCoin:
            params["settleCoin"] = settleCoin
        if orderId:
            params["orderId"] = orderId
        if orderLinkId:
            params["orderLinkId"] = orderLinkId
        if orderFilter:
            params["orderFilter"] = orderFilter
        if orderStatus:
            params["orderStatus"] = orderStatus
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
        if cursor:
            params["cursor"] = cursor

        # Convert params dictionary to url parameters
        payload = "&".join("{}={}".format(k, v) for k, v in params.items())

        method = "GET"
        response = self.send_http_rquest(end_point, method, payload)
        response = response.json()
        transaction_price = response['result']['list'][0]['avgPrice']

        return response, transaction_price

    # {'retCode': 0, 'retMsg': 'OK', 'result': {'nextPageCursor': '1482726557505117696', 'category': 'spot', 'list': [
    #     {'orderLinkId': '1691490779511842', 'orderId': '1482726557505117696', 'blockTradeId': '', 'symbol': 'ETHUSDC',
    #      'price': '1830.80', 'isLeverage': '0', 'positionIdx': 0, 'qty': '0.01000', 'side': 'Buy',
    #      'orderStatus': 'Filled', 'cancelType': 'UNKNOWN', 'rejectReason': '', 'avgPrice': '1828.79358',
    #      'leavesQty': '', 'leavesValue': '', 'cumExecQty': '0.01', 'cumExecValue': '', 'cumExecFee': '',
    #      'timeInForce': 'GTC', 'orderType': 'Limit', 'stopOrderType': '', 'orderIv': '', 'triggerPrice': '',
    #      'takeProfit': '', 'stopLoss': '', 'tpTriggerBy': '', 'slTriggerBy': '', 'triggerDirection': 0, 'triggerBy': '',
    #      'lastPriceOnCreated': '', 'reduceOnly': False, 'closeOnTrigger': False, 'createdTime': '1691490779518',
    #      'updatedTime': '1691490779556', 'smpType': 'None', 'smpGroup': 0, 'smpOrderId': ''}]}, 'retExtInfo': {},
    #  'time': 1691491412742}


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
        response = response.json()
        transaction_price = response['fills'][0]['price']

        return response, transaction_price

    # demo
    # {'symbol': 'BTCTUSD', 'orderId': 2268120203, 'orderListId': -1, 'clientOrderId': 'fchXV9USfkL3RA8XujgK6u',
    #  'transactTime': 1691059267646, 'price': '0.00000000', 'origQty': '0.00200000', 'executedQty': '0.00200000',
    #  'cummulativeQuoteQty': '58.30362000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY',
    #  'workingTime': 1691059267646, 'fills': [
    #     {'price': '29151.81000000', 'qty': '0.00200000', 'commission': '0.00000000', 'commissionAsset': 'BNB',
    #      'tradeId': 293530061}], 'selfTradePreventionMode': 'NONE'}

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
        response = response.json()

        binance_balances = {
            balance['asset']: balance['free']
            for balance in response['balances']
            if float(balance['free']) > 0
        }
        # print(json.dumps(account_info, indent=2))
        # print(positive_balances)
        return binance_balances

    def fetch_binance_data(self, binance_symbol):
        url = 'https://api.binance.com/api/v3/ticker/bookTicker'
        headers = {'X-MBX-APIKEY': pal.binance_key}
        response = requests.get(url, headers=headers)
        data = response.json()

        target_data = None
        for item in data:
            if item['symbol'] == binance_symbol:
                target_data = item
                break

        if target_data is None:
            raise ValueError(f'Symbol {binance_symbol} not found in the response data.')

        binance_ask_price = float(target_data['askPrice'])
        binance_bid_price = float(target_data['bidPrice'])
        # volume = None  # The bookTicker endpoint does not provide 24-hour trading volume.

        return binance_ask_price, binance_bid_price


class Bitget_Request:

    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.url = "https://api.bitget.com"

    def _generate_signature(self, message):
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

    def _generate_headers(self, timestamp, signature, method):

        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
            "ACCESS-METHOD": method
        }

    def set_position_mode(self, productType, mode):
        method = 'POST'
        request_path = "/api/mix/v1/account/setPositionMode"

        # Body of the request, in this case, it's not empty like in the GET requests
        body = json.dumps({"productType": productType, "holdMode": mode})

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))

        pre_hash_str = self.pre_hash(timestamp, method, request_path, str(body))
        signature = self._generate_signature(pre_hash_str)
        headers = self._generate_headers(timestamp, signature, method)

        url = self.url + request_path
        response = requests.post(url, data=body, headers=headers)
        response = response.json()

        # print(response.json())  # Log response
        return response

    def place_single_order(self, symbol, side, size, marginCoin, order_type='limit', price=None ):
        # self.set_position_mode('single_hold')

        method = 'POST'
        request_path = "/api/mix/v1/order/placeOrder"

        # Body of the request
        body = {
            "symbol": symbol,
            "marginCoin": marginCoin,
            "size": str(size),
            "side": side,
            "orderType": order_type
        }

        if order_type == 'limit':
            body['price'] = str(price)

        # Convert the body to JSON format
        body = json.dumps(body)

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        signature = self._generate_signature(pre_hash_str)
        headers = self._generate_headers(timestamp, signature, method)

        url = self.url + request_path
        response = requests.post(url, data=body, headers=headers)
        response = response.json()
        orderid = json.loads(response['data']['orderId'])

        print(f'order sent: {response}, param = {body}')  # Log response
        return orderid

    def get_open_orders(self, symbol):

        timestamp = str(int(time.time() * 1000))

        request_path = "/api/mix/v1/order/current"

        params = {'symbol': symbol}
        body = ""

        request_path += self.parse_params_to_str(params)

        message = self.pre_hash(timestamp, "GET", request_path, str(body))

        signature = self._generate_signature(message)

        headers = self._generate_headers("GET", timestamp, signature)
        params = {'symbol': symbol}
        url = "https://api.bitget.com/api/mix/v1/order/current"

        # print("HEADERS:", headers)
        # print("PARAMS:", params)
        # print(signature)


        response = requests.get(url, params=params, headers=headers)
        print(response.json())
        return response.json()


    def get_order_fills(self, symbol, order_id=None, start_time=None, end_time=None, last_end_id=None):
        method = 'GET'
        request_path = "/api/mix/v1/order/fills"

        # Add optional parameters to the request_path
        params = {'symbol': symbol}
        if order_id:
            params['orderId'] = order_id
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        if last_end_id:
            params['lastEndId'] = last_end_id

        # If there are parameters, add them to the request path
        if params:
            request_path += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        body = ''

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))
        # print("Timestamp:", timestamp)  # Log timestamp

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        # print("Pre-Hash String:", pre_hash_str)  # Log pre-hash string
        signature = self._generate_signature(pre_hash_str)
        # print("Signature:", signature.decode())

        headers = self._generate_headers(timestamp, signature, method)
        # print("Headers:", headers)  # Log headers

        url = self.url + request_path
        # print("URL:", url)  # Log URL
        response = requests.get(url, headers=headers)

        print(response.text)  # Log response
        return response.json()

    def get_order_detail(self, symbol, order_id=None, client_oid=None):
        method = 'GET'
        request_path = "/api/mix/v1/order/detail"

        # Add required and optional parameters to the request_path
        params = {'symbol': symbol}
        if order_id:
            params['orderId'] = str(order_id)
        if client_oid:
            params['clientOid'] = client_oid

        # If there are parameters, add them to the request path
        if params:
            request_path += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        body = ''

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))
        # print("Timestamp:", timestamp)  # Log timestamp

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        # print("Pre-Hash String:", pre_hash_str)  # Log pre-hash string
        signature = self._generate_signature(pre_hash_str)
        # print("Signature:", signature.decode())  # Log signature

        headers = self._generate_headers(timestamp, signature, method)
        # print("Headers:", headers)  # Log headers

        url = self.url + request_path
        # print("URL:", url)  # Log URL
        response = requests.get(url, headers=headers, timeout=1)
        response = response.json()
        filledQty = response['data']['filledQty']
        size = response['data']['size']
        state = response['data']['state'] #new > partially_filled > filled > canceled
        fee = response['data']['fee']

        # print(response)  # Log response
        return state, size, filledQty, fee
    #{'code': '00000', 'msg': 'success', 'requestTime': 1690443747093, 'data': {'symbol': 'BTCUSDT_UMCBL', 'size': 0.002, 'orderId': '1068363996764712962', 'clientOid': '1068363996768907264', 'filledQty': 0.0, 'fee': 0.0, 'price': 32000.0, 'state': 'new', 'side': 'sell_single', 'timeInForce': 'normal', 'totalProfits': 0.0, 'posSide': 'short', 'marginCoin': 'USDT', 'filledAmount': 0.0, 'orderType': 'limit', 'leverage': '1', 'marginMode': 'crossed', 'reduceOnly': False, 'enterPointSource': 'API', 'tradeSide': 'sell_single', 'holdMode': 'single_hold', 'orderSource': 'normal', 'cTime': '1690443746749', 'uTime': '1690443746749'}}

    def cancel_all_orders(self, symbol, margin_coin):
        method = 'POST'
        request_path = "/api/mix/v1/order/cancel-symbol-orders"

        # Body of the request
        body = {
            "symbol": symbol,
            "marginCoin": margin_coin
        }

        # Convert the body to JSON format
        body = json.dumps(body)

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        signature = self._generate_signature(pre_hash_str)
        headers = self._generate_headers(timestamp, signature, method)

        url = self.url + request_path
        response = requests.post(url, data=body, headers=headers)
        response = response.json()
        cancel_status = response['msg']

        print(f'order cancel: {response}')  # Log response
        return cancel_status

    # order cancel: {'code': '45130', 'msg': 'No order to cancel', 'requestTime': 1690316112174, 'data': None}

    def get_all_positions(self, product_type, margin_coin=None): #'umcbl'
        method = 'GET'
        request_path = "/api/mix/v1/position/allPosition-v2"

        # Add required and optional parameters to the request_path
        params = {'productType': product_type}
        if margin_coin:
            params['marginCoin'] = margin_coin

        # If there are parameters, add them to the request path
        if params:
            request_path += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        body = ''

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        signature = self._generate_signature(pre_hash_str)
        headers = self._generate_headers(timestamp, signature, method)

        url = self.url + request_path
        response = requests.get(url, headers=headers)
        response = response.json()

        # Initialize variables with default values
        holding_symbol = holding_side = holding_size = None

        try:
            holding_symbol = response['data'][0]['symbol']
            holding_side = response['data'][0]['holdSide']
            holding_size = response['data'][0]['total']
        except Exception as e:
            print(f'get all position error: {e}')

        # print(response)  # Log response
        return response, holding_symbol, holding_side, holding_size

    # demo
    # {'code': '00000', 'msg': 'success', 'requestTime': 0, 'data': [{'marginCoin': 'USDT', 'symbol': 'BTCUSDT_UMCBL', 'holdSide': 'short', 'openDelegateCount': '0', 'margin': '29.81', 'available': '0.001', 'locked': '0', 'total': '0.001', 'leverage': 1, 'achievedProfits': '0', 'averageOpenPrice': '29810', 'marginMode': 'crossed', 'holdMode': 'single_hold', 'unrealizedPL': '0.00059', 'liquidationPrice': '229654.990714', 'keepMarginRate': '0.004', 'marketPrice': '29809.41', 'marginRatio': '0.000685675728', 'cTime': '1689786992290'}]}
    # {'code': '00000', 'msg': 'success', 'requestTime': 0, 'data': [{'marginCoin': 'USDT', 'symbol': 'BTCUSDT_UMCBL', 'holdSide': 'long', 'openDelegateCount': '0', 'margin': '29.8225', 'available': '0.001', 'locked': '0', 'total': '0.001', 'leverage': 1, 'achievedProfits': '0', 'averageOpenPrice': '29822.5', 'marginMode': 'crossed', 'holdMode': 'single_hold', 'unrealizedPL': '-0.00024', 'liquidationPrice': '-169974.144604', 'keepMarginRate': '0.004', 'marketPrice': '29822.26', 'marginRatio': '0.000686139824', 'cTime': '1689786992290'}]}
    # {'code': '00000', 'msg': 'success', 'requestTime': 0, 'data': []}

    def get_symbol_position_v2(self, symbol, margin_coin):
        method = 'GET'
        request_path = "/api/mix/v1/position/singlePosition-v2"

        # Add required parameters to the request_path
        params = {'symbol': symbol, 'marginCoin': margin_coin}

        # If there are parameters, add them to the request path
        if params:
            request_path += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        body = ''

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        signature = self._generate_signature(pre_hash_str)
        headers = self._generate_headers(timestamp, signature, method)

        url = self.url + request_path
        response = requests.get(url, headers=headers)
        response = response.json()

        # Initialize variables with default values
        holding_symbol = holding_side = holding_size = None

        try:
            holding_symbol = response['data'][0]['symbol']
            holding_side = response['data'][0]['holdSide']
            holding_size = response['data'][0]['total']
        except Exception as e:
            print(f'get all position error: {e}')

        # print(f'bitget position: {response}')  # Log response
        return response, holding_symbol, holding_side, holding_size

    #{'code': '00000', 'msg': 'success', 'requestTime': 0, 'data': [{'marginCoin': 'USDT', 'symbol': 'BTCUSDT_UMCBL', 'holdSide': 'long', 'openDelegateCount': '0', 'margin': '0', 'available': '0', 'locked': '0', 'total': '0', 'leverage': 1, 'achievedProfits': None, 'averageOpenPrice': None, 'marginMode': 'crossed', 'holdMode': 'single_hold', 'unrealizedPL': None, 'liquidationPrice': None, 'keepMarginRate': None, 'marketPrice': None, 'marginRatio': None, 'cTime': None}, {'marginCoin': 'USDT', 'symbol': 'BTCUSDT_UMCBL', 'holdSide': 'short', 'openDelegateCount': '0', 'margin': '0', 'available': '0', 'locked': '0', 'total': '0', 'leverage': 1, 'achievedProfits': None, 'averageOpenPrice': None, 'marginMode': 'crossed', 'holdMode': 'single_hold', 'unrealizedPL': None, 'liquidationPrice': None, 'keepMarginRate': None, 'marketPrice': None, 'marginRatio': None, 'cTime': None}]}

    def get_account_list(self, product_type):
        method = 'GET'
        request_path = "/api/mix/v1/account/accounts"
        params = {'productType': product_type}

        # If there are parameters, add them to the request path
        if params:
            request_path += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

        body = ''

        # Generate the timestamp just before the request
        timestamp = str(round(pytz.utc.localize(datetime.utcnow()).timestamp() * 1000))
        # print("Timestamp:", timestamp)  # Log timestamp

        pre_hash_str = self.pre_hash(timestamp, method, request_path, body)
        # print("Pre-Hash String:", pre_hash_str)  # Log pre-hash string
        signature = self._generate_signature(pre_hash_str)
        # print("Signature:", signature.decode())  # Log signature

        headers = self._generate_headers(timestamp, signature, method)
        # print("Headers:", headers)  # Log headers

        url = self.url + request_path
        # print("URL:", url)  # Log URL
        response = requests.get(url, headers=headers)

        print(response.json())  # Log response
        return response.json()

    # demo
    # {'code': '00000', 'msg': 'success', 'requestTime': 1690031660001, 'data': [{'marginCoin': 'USDT', 'locked': '0', 'available': '199.8378682', 'crossMaxAvailable': '199.8378682', 'fixedMaxAvailable': '199.8378682', 'maxTransferOut': '199.8378682', 'equity': '199.8378682', 'usdtEquity': '199.8378682', 'btcEquity': '0.006694351569', 'crossRiskRate': '0', 'unrealizedPL': '0', 'bonus': '0'}]}
    # {'code': '00000', 'msg': 'success', 'requestTime': 1690032000347, 'data': [{'marginCoin': 'USDT', 'locked': '0', 'available': '199.8020638', 'crossMaxAvailable': '140.1290438', 'fixedMaxAvailable': '140.1290438', 'maxTransferOut': '140.1280638', 'equity': '199.8030438', 'usdtEquity': '199.8030438', 'btcEquity': '0.00669203366', 'crossRiskRate': '0.001373877509', 'unrealizedPL': '0.00098', 'bonus': '0'}]}

    def fetch_bitget_data(self, symbol):
        url = "https://api.bitget.com/api/mix/v1/market/ticker"
        querystring = {"symbol": symbol}

        response = requests.get(url, params=querystring)
        data = response.json()

        if data["code"] == "00000" and "data" in data:
            target_data = data["data"]
        else:
            raise ValueError(f'Symbol {symbol} not found in the response data.')

        ask_price = float(target_data["bestAsk"])
        bid_price = float(target_data["bestBid"])
        ask_size = float(target_data["askSz"])
        bid_size = float(target_data["bidSz"])
        # print(data)

        return ask_price, bid_price, ask_size, bid_size

        # {'code': '00000', 'msg': 'success', 'requestTime': 1691223918718,
        #  'data': {'symbol': 'BTCUSDT_UMCBL', 'last': '29037.5', 'bestAsk': '29037.5', 'bestBid': '29037',
        #           'bidSz': '3.101', 'askSz': '24.263', 'high24h': '29310', 'low24h': '28781',
        #           'timestamp': '1691223918718', 'priceChangePercent': '-0.0072', 'baseVolume': '102788.4',
        #           'quoteVolume': '2992163292.966', 'usdtVolume': '2992163292.966', 'openUtc': '29092',
        #           'chgUtc': '-0.00189', 'indexPrice': '29048.349473', 'fundingRate': '0.000099',
        #           'holdingAmount': '84241.025', 'deliveryStartTime': None, 'deliveryTime': None,
        #           'deliveryStatus': 'normal'}}
