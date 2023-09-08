import requests
import pandas as pd
import os
import time
from datetime import datetime
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

def get_book_summary_by_currency(currency, kind=None):
    base_url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
    params = {
        "currency": currency,
        "kind": kind
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

def fetch_and_append_data():
    currency = "ETH"
    kind = "future"

    try:
        response = get_book_summary_by_currency(currency, kind)
    except Exception as e:
        print(e)
        return

    headers = []
    data = []

    for item in response:
        if 'ETH' in item['instrument_name']:
            headers.append(item['instrument_name'])
            data.append(item['mark_price'])

    closest_contract = min(headers, key=days_until_contract_date)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data_dict = {'timestamp': [timestamp]}
    data_dict.update({header: [value] for header, value in zip(headers, data)})

    data_dict.update(calculate_price_differences(data_dict, headers))

    df = pd.DataFrame(data_dict)

    csv_file = "ETH_future_price_diff_deribit.csv"

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="w", header=True, index=False)
    else:
        df.to_csv(csv_file, mode="a", header=False, index=False)

    print(df)

def calculate_price_differences(data_dict, eth_contracts):
    reference_contracts = ['ETH-PERPETUAL']

    reference_prices = {contract: float(data_dict[contract][0]) for contract in reference_contracts}

    price_differences = {}
    for contract in eth_contracts:
        if contract in data_dict:
            contract_price = float(data_dict[contract][0])
            for ref_contract, ref_price in reference_prices.items():
                price_difference = contract_price - ref_price
                column_name = f"{contract}_vs_{ref_contract}"
                price_differences[column_name] = [price_difference]

    return price_differences

interval = 60

while True:
    try:
        fetch_and_append_data()
        time.sleep(interval)
    except:
        continue