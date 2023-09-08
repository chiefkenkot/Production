import json
import time
import csv
import requests_html
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
from pprint import pprint

date = datetime.datetime.now().date()


###### 新資金 ######
def new_fund():
    url = 'https://www.airstarbank.com/deposit_rate.json'
    response = requests.get(url)
    data = json.loads(response.text)

    # pprint(data)
    # pprint(data[4])

    header = data[4]['currency']
    table = data[4]['tenors']

    # Extract the time deposit rates for HKD
    hkd_time_deposit = None
    for item in data:
        if item['currency']['code'] == 'HKD' and item['rate_type'] == 'Time Deposit Rate':
            hkd_time_deposit = item
            break

    # Extract the tenors and rates
    tenors = [item['en'] for item in hkd_time_deposit['tenors']]
    rates = [item['rate'] for item in hkd_time_deposit['tenors']]

    # Print the table
    with open(f'{date}_Air_Star.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['HKD'])
        writer.writerow(['Tenor', 'Rate'])
        for i in range(len(tenors)):
            writer.writerow([tenors[i], rates[i]])


new_fund()



