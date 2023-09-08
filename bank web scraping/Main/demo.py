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

date = datetime.datetime.now().date()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def hsbc_existing_client():
    url = 'https://www.hsbc.com.hk/zh-hk/investments/market-information/hk/deposit-rate/#hkd'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    normal_rate_table = soup.find(id='content_main_columnControlColumn_23')


    # Extract the table data
    # data = [['004_HSBC', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000-999,999', '港元 1,000,000 以上']]
    data = []
    header = normal_rate_table
    # headers = [header.text.strip() for header in header.find_all('th')][0:5]
    # data.append(headers)
    rows = header.find_all('tr')
    # print(headers[0:5])


    for row in rows[1:]:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        # if len(cells) == 5:
        if '一個月' in cells:
            # cells = cells[:-1] # remove 1m+ rate
            data.append(cells)
        elif '三個月' in cells:
            # cells = cells[:-1] # remove 1m+ rate
            data.append(cells)
        elif '六個月' in cells:
            # cells = cells[:-1] # remove 1m+ rate
            data.append(cells)
        elif '九個月' in cells:
            # cells = cells[:-1] # remove 1m+ rate
            data.append(cells)
        elif '十二個月' in cells:
            # cells = cells[:-1] # remove 1m+ rate
            data.append(cells)

    data = data[:-5]
    hsbc = data
    # hsbc = pd.DataFrame(data)

    print(hsbc)
    return hsbc

hsbc_existing_client()

# [['一個月', '0.6250%', '0.6250%', '0.6250%', '0.6750%'], ['三個月', '0.6500%', '0.6500%', '0.6500%', '0.7000%'], ['六個月', '0.6750%', '0.6750%', '0.6750%', '0.7250%'], ['九個月', '0.6750%', '0.6750%', '0.6750%', '0.7250%'], ['十二個月', '0.7000%', '0.7000%', '0.7000%', '0.7500%']]

def boc_existing_client():

    url = 'https://www.bochk.com/whk/rates/depositRates/depositRates-input.action?lang=hk'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find('table', class_='import-data width-100-percent small-font-text')
    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    data = [['012_BOC', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000-999,999', '港元 1,000,000 以上']]
    for row in rows:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if '1 個月' in cells:
            data.append(cells)
        elif '3 個月' in cells:
            data.append(cells)
        elif '6 個月' in cells:
            data.append(cells)
        elif '9 個月' in cells:
            data.append(cells)
        elif '12 個月' in cells:
            data.append(cells)
        # cells = row.find_all('td')
        # cells = [cell.text.strip() for cell in cells]
        # data.append(cells)


    # boc = pd.DataFrame(data)
    boc = data
    print(boc)
    return boc

def sc_existing_client():

    url = 'https://www.sc.com/hk/zh/deposits/board-rates/'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find(id='table-content-28993-3')

    # header = []
    # thead = hkd_table.find('thead').find('tr')
    #
    # for th in thead.findAll('th'):
    #     th = th.text.strip().replace('\n', '')
    #     header.append(th)

    # print(header)

    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    # data = [header]
    data = []
    for row in rows:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if '1個月' in cells:
            data.append(cells)
        elif '3個月' in cells:
            data.append(cells)
        elif '6個月' in cells:
            data.append(cells)
        elif '9個月' in cells:
            data.append(cells)
        elif '12個月' in cells:
            data.append(cells)
    # cols = row.find_all('td')
    # cols = [col.text.strip() for col in cols]
    # data.append(cols)
    data = [[row[i] for i in [0, 2, 3, 4, 5]] for row in data]
    data.insert(0, ['003_SC', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000-999,999', '港元 1,000,000 以上'])
    sc = pd.DataFrame(data)

    print(sc)
    return sc

def airstar_existing_client(): # no amount provided
    url = 'https://www.airstarbank.com/deposit_rate.json'
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract the time deposit rates for HKD
    hkd_time_deposit = None
    for item in data:
        if item['currency']['code'] == 'HKD' and item['rate_type'] == 'Time Deposit Rate':
            hkd_time_deposit = item
            break

    # Extract the tenors and rates
    tenors = [item['en'] for item in hkd_time_deposit['tenors']]
    rates = [item['rate'] for item in hkd_time_deposit['tenors']]

    # Remove 1 week and 2 months data from tenors and rates
    exclude_tenors = ['1 week', '2 months']
    tenors = [tenor for tenor in tenors if tenor not in exclude_tenors]
    rates = [rate for tenor, rate in zip(tenors, rates) if tenor not in exclude_tenors]

    # Prepare the data
    # columns = ['Tenor', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000-999,999', '港元 1,000,000 以上']
    data = list(zip(tenors, rates, rates, rates, rates))

    # Insert the bank name and tenor information as the first row
    data.insert(0, (
    '395_AirStar', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000-999,999', '港元 1,000,000 以上'))

    # Create a DataFrame with the data
    airstar = pd.DataFrame(data)
    print(airstar)
    return airstar