
import time
import hmac
import hashlib
import requests

class ByBitRequest:
    def __init__(self) -> None:
        pass
    
    def set_up(self,api_key,secret_key,recv_windows,url_path):
        self.api_key=api_key
        self.secret_key=secret_key
        self.httpClient=requests.Session()
        self.recv_window=recv_windows
        self.url_path=url_path # Testnet endpoint
    
    def gen_signature(self,time_stamp,payload):
        param_str= str(time_stamp) + self.api_key + self.recv_window + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def send_http_rquest(self,end_point,method,payload):
        time_stamp=str(int(time.time() * 10 ** 3))
        signature=self.gen_signature(time_stamp,payload)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }
        
        if(method=="POST"):
            response = self.httpClient.request(method, self.url_path+end_point, headers=headers, data=payload)
        else:
            response = self.httpClient.request(method, self.url_path+end_point+"?"+payload, headers=headers)
        
        print(end_point + " Elapsed Time : " + str(response.elapsed))
        return response.text
    
    
    def get_market_price(self,category,symbol):
        end_point = "/v5/market/orderbook"
        params_fomat = "category={category_value}&symbol={symbol_value}"
        params = params_fomat.format(category_value = category, symbol_value = symbol)
        method="GET"
        response = self.send_http_rquest(end_point,method,params)
        return response
    
    def get_wallet_balance(self,account_type,coin = ""):
        end_point = "/v5/account/wallet-balance"
        params_fomat = "accountType={accountType_value}&coin={coin_value}"
        if(coin == ""):
            params_fomat = "accountType={accountType_value}"
            params = params_fomat.format(accountType_value = account_type)
        else:
            params = params_fomat.format(accountType_value = account_type,coin_value = coin)
       
        method="GET"
        response = self.send_http_rquest(end_point,method,params)
        return response



    def get_open_orders(self, category):
        end_point = "/v5/order/open-order"
        params_format = "category={category}"
        params = params_format.format(category=category)

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


    def place_market_order(self, category, side, symbol, order_type, qty,is_leverage, order_filter):
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

