import time
import json
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import re
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def days_until_contract_date(symbol):
    today = datetime.today()
    contract_date_str = re.search(r'\d{2}[A-Z]{3}\d{2}', symbol)
    if contract_date_str:
        contract_date = datetime.strptime(contract_date_str.group(), '%d%b%y')
        days_until = (contract_date - today).days
        print(days_until)
        return days_until
    return float("inf")


def fetch_and_append_data():
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {'category': 'linear'}
    response = requests.get(url, params=params)
    response = json.loads(response.text)['result']['list']

    headers = []
    data = []

    for item in response:
        if 'BTC' in item['symbol']:
            headers.append(item['symbol'])
            data.append(item['markPrice'])

    closest_contract = min(headers, key=days_until_contract_date)
    print(f"Closest contract: {closest_contract}")

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
    csv_file = "BTC future price diff.csv"

    # Check if the file exists, if not, create it with headers
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    # print(headers)
    # print(data)
    print(df)

    return data_dict

def calculate_price_differences(data_dict, btc_contracts):
    # reference_contracts = ['BTCPERP', 'BTCUSDT']
    reference_contracts = ['BTCUSDT']

    # Get prices for reference contracts
    reference_prices = {contract: float(data_dict[contract][0]) for contract in reference_contracts}

    price_differences = {}
    for contract in btc_contracts:
        if contract in data_dict:
            contract_price = float(data_dict[contract][0])
            for ref_contract, ref_price in reference_prices.items():
                price_difference = contract_price - ref_price
                column_name = f"{contract}_vs_{ref_contract}"
                price_differences[column_name] = [price_difference]

    return price_differences

# Set an interval (in seconds)
interval = 5

while True:
    data_dict = fetch_and_append_data()
    time.sleep(interval)