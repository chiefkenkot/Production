import json
import time
import csv
import requests_html
from requests_html import HTMLSession
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

# main_header = ['存款期', '港元 10,000-99,999', '港元 100,000-499,999', '港元 500,000 以上']
# 年期 = 1 個月 / 3 個月 / 6 個月 / 9 個月 / 12 個月


def hsbc_existing_client():
    url = 'https://www.hsbc.com.hk/zh-hk/investments/market-information/hk/deposit-rate/#hkd'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    normal_rate_table = soup.find(id='content_main_columnControlColumn_23')

    data = []
    rows = normal_rate_table.find_all('tr')

    tenor_mapping = {'一個月': '1m', '三個月': '3m', '六個月': '6m', '九個月': '9m', '十二個月': '12m'}

    for row in rows[1:]:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if any(tenor in cells for tenor in tenor_mapping.keys()):
            # Replace Chinese tenor with numerical representation in months
            tenor = tenor_mapping[cells[0]]
            # Remove '%' sign, convert to float, round to 5 digits and create a new list of cells
            cells = [4] + [tenor] + [round(float(cell[:-1]) / 100, 5) if '%' in cell else cell for cell in cells[1:]]
            data.append(cells)

    # Remove the last five rows
    hsbc = data[:-5]

    # Create a DataFrame
    # hsbc = pd.DataFrame(data)
    print(hsbc)
    return hsbc


def boc_existing_client():
    url = 'https://www.bochk.com/whk/rates/depositRates/depositRates-input.action?lang=hk'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find('table', class_='import-data width-100-percent small-font-text')
    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    data = []
    tenor_mapping = {'1 個月': '1m', '3 個月': '3m', '6 個月': '6m', '9 個月': '9m', '12 個月': '12m'}

    for row in rows:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if any(tenor in cells for tenor in tenor_mapping.keys()):
            # Replace Chinese tenor with numerical representation in months
            tenor = tenor_mapping[cells[0]]
            # Remove '%' sign, convert to float, round to 5 digits and create a new list of cells
            cells = [12] + [tenor] + [round(float(cell[:-1]) / 100, 5) if '%' in cell else cell for cell in cells[1:]]
            cells.insert(4, cells[3])
            data.append(cells)


    boc = data
    print(boc)
    return boc


def sc_existing_client():
    url = 'https://www.sc.com/hk/zh/deposits/board-rates/'
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find(id='table-content-28993-3')

    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    data = []
    tenor_mapping = {'1個月': '1m', '3個月': '3m', '6個月': '6m', '9個月': '9m', '12個月': '12m'}

    for row in rows:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if any(tenor in cells for tenor in tenor_mapping.keys()):
            # Replace Chinese tenor with numerical representation in months
            tenor = tenor_mapping[cells[0]]
            # Remove '%' sign, convert to float, round to 5 digits and create a new list of cells
            cells = [3] + [tenor] + [round(float(cell[:-1]) / 100, 5) if '%' in cell else cell for cell in cells[2:6]]
            data.append(cells)

    sc = data

    print(sc)
    return sc



def airstar_existing_client():  # no amount provided
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
    tenor_mapping = {'1 month': '1m', '3 months': '3m', '6 months': '6m', '9 months': '9m', '12 months': '12m'}
    data = []
    for tenor, rate in zip(tenors, rates):
        if tenor in tenor_mapping.keys():
            rate_float = float(rate[:-1])  # Convert rate to float after removing the percentage sign
            cells = [395] + [tenor_mapping[tenor]] + [round(rate_float / 100, 5)] * 4
            data.append(cells)

    airstar = data
    print(airstar)
    return airstar

# airstar_existing_client()


def dbs_existing_client():
    url = 'https://www.dbs.com.hk/personal-zh/promotion/OnlineTD-promo'

    session = requests_html.HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, "html.parser")

    hkd_table = soup.find('table', class_='currency_table HKD')
    hkd_rows = hkd_table.findAll('tr')

    # Extract data from the table
    data = []
    for row in hkd_rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        if len(cols) > 1:
            tenor = cols[0]
            rate = cols[1]
            data.append((tenor, rate))

    # Prepare the data
    tenor_mapping = {'1個月': '1m', '3個月': '3m', '6個月': '6m', '12個月': '12m'}
    result = []
    for tenor, rate in data:
        if tenor in tenor_mapping.keys():
            rate_float = float(rate[:-1])  # Convert rate to float after removing the percentage sign
            rate_float = round(rate_float / 100, 5)
            cells = [16, tenor_mapping[tenor], rate_float, rate_float, rate_float, rate_float]
            result.append(cells)

    # Add None value for the 9-month tenor
    result.insert(3, [16, '9m', None, None, None, None])

    print(result)
    return result

dbs_existing_client()

# def za_existing_client():
#     url = 'https://bank.za.group/hk/deposit'
#
#     session = requests_html.HTMLSession()
#
#     response = session.get(url)
#     response.html.render()
#     soup = BeautifulSoup(response.html.html, "html.parser")
#
#     hkd_table = soup.findAll('div', class_='InterestQueryTable_tabContent__onTgG')
#
#     print(hkd_table)
#
#     # header = []
#     # thead = hkd_table.find('thead').find('tr')
#     #
#     # for th in thead.findAll('th'):
#     #     th = th.text.strip()
#     #     header.append(th)
#     #
#     # print(header)
#
#     # hkd_rows = hkd_table.findAll('tr')
#     #
#     # # Find the table element and extract the data
#     # rows = hkd_rows
#     # data = []
#     # for row in rows:
#     #     cols = row.find_all('td')
#     #     cols = [col.text.strip() for col in cols]
#     #     data.append(cols)
#     #
#     #
#     # print(data)
#
# za_existing_client()





def fusion_existing_client():
    url = 'https://www.fusionbank.com/deposit.html?lang=tc'

    session = requests_html.HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, "html.parser")

    rate_table = soup.find('table', class_='deposit-table')
    rate_rows = rate_table.findAll('tr')

    # Extract data from the table
    data = []
    tenor_mapping = {'1 個月': '1m', '3 個月': '3m', '6 個月': '6m', '12 個月': '12m'}

    for row in rate_rows:
        cols = row.find_all(['td', 'th'])
        cols = [col.text.strip().replace('\n', '') for col in cols]
        if any(tenor in cols for tenor in tenor_mapping.keys()):
            data.append(cols)

    # Only keep the data for 1, 3, 6, and 12 months
    filtered_data = [row for row in data if row[0] in ['1 個月', '3 個月', '6 個月', '12 個月']]

    # Convert to the desired format
    formatted_data = []
    bank_code = 391
    for row in filtered_data:
        tenor = tenor_mapping[row[0]]
        rates = [round(float(rate[:-1]) / 100, 5) for rate in row[1:]]
        formatted_row = [bank_code, tenor] + rates
        formatted_data.append(formatted_row)

    formatted_data.insert(3, [391, '9m', 'None', 'None', 'None', 'None'])

    print(formatted_data)
    return formatted_data

fusion_existing_client()
