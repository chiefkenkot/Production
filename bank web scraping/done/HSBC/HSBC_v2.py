import csv
import datetime
import time

import requests_html
from bs4 import BeautifulSoup

date = datetime.datetime.now().date()
print(date)



def new_fund():
    url = 'https://www.hsbc.com.hk/zh-hk/accounts/offers/deposits/#3'

    session = requests_html.HTMLSession()

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find(id='content_main_basicTable_3')

    hkd_rows = hkd_table.findAll('tr')

    caption = soup.find('caption').text.strip()
    # print(caption)

    # Create a new list to store the data
    data = [['Bank Name', 'Currency', 'Tenor', 'Interest Rate', 'Remarks']]

    for row in hkd_rows:
        cells = row.find_all('td') + row.find_all('th')
        row_data = [cell.text.strip() for cell in cells]
        if len(row_data) == 5:
            data.append(row_data)

    # Write the data to a CSV file
    with open(f'{date}deposit_rates.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

###############################

###### 現有客戶 ######

def current_client():
    url = 'https://www.hsbc.com.hk/zh-hk/investments/market-information/hk/deposit-rate/#hkd'

    session = requests_html.HTMLSession()

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    normal_rate_table = soup.find(id='content_main_columnControlColumn_23')

    # Extract the table data
    data = []
    header = normal_rate_table
    headers = [header.text.strip() for header in header.find_all('th')][0:5]
    data.append(headers)
    # rows = header.find_all('tr')
    rows = normal_rate_table.find_all('tr')

    for row in rows[1:]:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if len(row_data) == 5:
            data.append(row_data)
        data.append(cells)

    # Write the data to a CSV file
    with open(f'{date}deposit_rates.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Call the functions
new_fund()
current_client()