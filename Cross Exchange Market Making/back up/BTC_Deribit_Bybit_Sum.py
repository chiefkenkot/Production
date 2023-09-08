import time
import json
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def days_until_contract_date(symbol):
    today = datetime.today()
    contract_date_str = re.search(r'\d{2}[A-Z]{3}\d{2}', symbol)
    if contract_date_str:
        contract_date = datetime.strptime(contract_date_str.group(), '%d%b%y')
        days_until = (contract_date - today).days
        return days_until
    return float("inf")

def get_book_summary_by_currency():
    url = "https://test.deribit.com/api/v2/public/get_book_summary_by_currency"
    params = {"currency": "BTC", "kind": "future"}
    response = requests.get(url, params=params)
    return response.json()["result"]

def fetch_and_append_data():
    # Fetch data from Deribit
    deribit_data = get_book_summary_by_currency()
    deribit_headers = ['Deribit_' + item["instrument_name"] for item in deribit_data]
    deribit_prices = [item["mark_price"] for item in deribit_data]

    # Fetch data from Bybit
    bybit_url = 'https://api.bybit.com/v5/market/tickers'
    bybit_params = {'category': 'linear'}
    bybit_response = requests.get(bybit_url, params=bybit_params)
    bybit_response = json.loads(bybit_response.text)['result']['list']

    bybit_headers = []
    bybit_data = []

    for item in bybit_response:
        if 'BTC' in item['symbol']:
            bybit_headers.append('Bybit_' + item['symbol'])
            bybit_data.append(item['markPrice'])

    # Merge headers and prices
    headers = deribit_headers + bybit_headers
    data = deribit_prices + bybit_data

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add the timestamp to the data dictionary
    data_dict = {'timestamp': [timestamp]}
    data_dict.update({header: [value] for header, value in zip(headers, data)})

    # Calculate price differences and add them to the data dictionary
    data_dict.update(calculate_price_differences(data_dict, headers))

    # Create a DataFrame using the dictionary
    df = pd.DataFrame(data_dict)

    # Append the DataFrame to a CSV file
    csv_file = "BTC_future_price_diff_merged.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

    return data_dict

def calculate_price_differences(data_dict, btc_contracts):
    reference_contracts = {
        'Deribit': 'Deribit_BTC-PERPETUAL',
        'Bybit': 'Bybit_BTCUSDT'
    }

    # Get prices for reference contracts
    reference_prices = {exchange: float(data_dict[contract][0]) for exchange, contract in reference_contracts.items()}

    price_differences = {}
    for contract in btc_contracts:
        if contract in data_dict:
            contract_price = float(data_dict[contract][0])
            for exchange, ref_contract in reference_contracts.items():
                if contract.startswith(exchange):
                    ref_price = reference_prices[exchange]
                    price_difference = contract_price - ref_price
                    column_name = f"{contract}_vs_{ref_contract}"
                    price_differences[column_name] = [price_difference]

    return price_differences

# Set an interval (in seconds)
interval = 60

while True:
    try:
        data_dict = fetch_and_append_data()
        time.sleep(interval)
    except:
        print('time out')
        continue