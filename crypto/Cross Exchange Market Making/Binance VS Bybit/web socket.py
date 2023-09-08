# import time
# import hmac
# import hashlib
# import json
# from websocket import create_connection, WebSocketApp
# import pal
#
# api_key = pal.bybit_key
# api_secret = pal.bybit_secret
#
# # Generate expires.
# expires = int((time.time() + 1) * 1000)
#
# # Generate signature.
# signature = hmac.new(
#     bytes(api_secret, 'utf-8'),
#     bytes(f"GET/realtime{expires}", 'utf-8'),
#     hashlib.sha256
# ).hexdigest()
#
# # Initialize an empty order book
# order_book = {"bids": {}, "asks": {}}
#
# def on_open(ws):
#     print("WebSocket connection is open.")
#
#     # Authenticate with API.
#     ws.send(json.dumps({
#         "op": "auth",
#         "args": [api_key, expires, signature]
#     }))
#
#     # Subscribe to the orderbook stream of BTCUSDT
#     ws.send(json.dumps({
#         "op": "subscribe",
#         "args": ["orderbook.1.BTCUSDT"]
#     }))
#
#
# def on_message(ws, message):
#     global order_book
#     data = json.loads(message)
#
#     if data['type'] == 'snapshot':
#         # Replace the entire local order book with the snapshot
#         order_book = {
#             "bids": {price: float(volume) for price, volume in data['data']['b']},
#             "asks": {price: float(volume) for price, volume in data['data']['a']},
#         }
#     elif data['type'] == 'delta':
#         # Update the local order book with the changes in the delta
#         for price, volume in data['data']['b']:
#             if volume == '0':
#                 del order_book['bids'][price]
#             else:
#                 order_book['bids'][price] = float(volume)
#         for price, volume in data['data']['a']:
#             if volume == '0':
#                 del order_book['asks'][price]
#             else:
#                 order_book['asks'][price] = float(volume)
#
#     # Print the top bid and ask prices
#     top_bid = max(order_book['bids'], key=float)
#     top_ask = min(order_book['asks'], key=float)
#     print(f"Top bid: {top_bid}, volume: {order_book['bids'][top_bid]}")
#     print(f"Top ask: {top_ask}, volume: {order_book['asks'][top_ask]}")
#
# def on_close(ws, close_status_code, close_msg):
#     print("WebSocket connection is closed.")
#
# def on_error(ws, error):
#     print("Error: %s" % error)
#
# # Connect to WebSocket.
# ws = WebSocketApp(
#     "wss://stream.bybit.com/v5/public/spot",
#     on_open=on_open,
#     on_message=on_message,
#     on_close=on_close,
#     on_error=on_error
# )
#
# ws.run_forever()

# ======================================================

# import threading
# import time
# import hmac
# import hashlib
# import json
# from websocket import create_connection, WebSocketApp
# import pal
#
# api_key = pal.bybit_key
# api_secret = pal.bybit_secret
#
# # Execution data will be stored here
# execution_data = None
#
# def on_message(ws, message):
#     global execution_data
#     data = json.loads(message)
#
#     if data['topic'] == 'execution':
#         # Store the execution data
#         execution_data = data['data']
#
#         # Close the WebSocket connection after receiving the execution data
#         ws.close()
#
# # This function will run in a separate thread
# def websocket_thread():
#     # Generate expires.
#     expires = int((time.time() + 1) * 1000)
#     # Generate signature.
#     signature = hmac.new(
#         bytes(api_secret, 'utf-8'),
#         bytes(f"GET/realtime{expires}", 'utf-8'),
#         hashlib.sha256
#     ).hexdigest()
#
#     # Connect to WebSocket.
#     ws = WebSocketApp(
#         "wss://stream.bybit.com/v5/private",  # Private endpoint for user data streams
#         on_message=on_message
#     )
#
#     # Authenticate with API.
#     ws.send(json.dumps({
#         "op": "auth",
#         "args": [api_key, expires, signature]
#     }))
#
#     # Subscribe to the execution stream
#     ws.send(json.dumps({
#         "op": "subscribe",
#         "args": ["execution"]
#     }))
#
#     ws.run_forever()
#
# # Start the WebSocket in a separate thread
# threading.Thread(target=websocket_thread).start()
#
# # Wait for a bit to ensure the execution data has been received
# time.sleep(1)
#
# # Now your trading logic can use the data in `execution_data`
# print("Execution data: ", execution_data)


# ======================================================

# import time
# import hmac
# import hashlib
# import json
# from websocket import create_connection, WebSocketApp
# import pal
#
# api_key = pal.bybit_key
# api_secret = pal.bybit_secret
#
# # Generate expires.
# expires = int((time.time() + 1) * 1000)
#
# # Generate signature.
# signature = hmac.new(
#     bytes(api_secret, 'utf-8'),
#     bytes(f"GET/realtime{expires}", 'utf-8'),
#     hashlib.sha256
# ).hexdigest()
#
# def on_open(ws):
#     print("WebSocket connection is open.")
#
#     # Authenticate with API.
#     ws.send(json.dumps({
#         "op": "auth",
#         "args": [api_key, expires, signature]
#     }))
#
#     # Subscribe to the order stream
#     ws.send(json.dumps({
#         "op": "subscribe",
#         "args": ["order"]
#     }))
#
# def on_message(ws, message):
#     data = json.loads(message)
#     if 'topic' in data:
#         if data['topic'] == 'order':
#             print("Order data: ", data['data'])
#     else:
#         print("Received message without 'topic': ", data)
#
# def on_close(ws, close_status_code, close_msg):
#     print("WebSocket connection is closed.")
#
# def on_error(ws, error):
#     print("Error: %s" % error)
#
# # Connect to WebSocket.
# ws = WebSocketApp(
#     "wss://stream.bybit.com/v5/private",  # Private endpoint for user data streams
#     on_open=on_open,
#     on_message=on_message,
#     on_close=on_close,
#     on_error=on_error
# )
#
# ws.run_forever()

# ======================================================

import hmac
import time
import json
import threading
from websocket import create_connection
import websocket
import pal

# Replace these with your API credentials.
api_key = pal.bybit_key
api_secret = pal.bybit_secret

# Define WebSocket URL.
url = "wss://stream.bybit.com/v5/private"

# Generate expires.
expires = int((time.time() + 1) * 1000)

# Generate signature.
signature = str(hmac.new(
    bytes(api_secret, "utf-8"),
    bytes(f"GET/realtime{expires}", "utf-8"), digestmod="sha256"
).hexdigest())

# Create WebSocket connection.
# ws = create_connection(url=url)
ws = websocket.WebSocketApp(url=url)

# Authenticate with API.
ws.send(json.dumps({
    "op": "auth",
    "args": [api_key, expires, signature]
}))

# Subscribe to order updates.
ws.send(json.dumps({
    "op": "subscribe",
    "args": ["order"]
}))

ws = websocket()