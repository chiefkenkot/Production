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
from selenium import webdriver

date = datetime.datetime.now().date()


url = 'https://www.hangseng.com/zh-hk/personal/banking/rates/deposit-interest-rates/#rwd-tabs-with-accordion-1666825230-1-content'

# driver.get(url)
#
# hkd = driver.find_element(By.ID, 'rwd-table-40828760783')

# print(hkd)

###### 新資金 ######


session = requests_html.HTMLSession()

response = session.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# hkd_table = soup.find('table', class_='rwd-table rwd-table')
hkd_table = soup.find(id='rwd-table-582937964508')
print(hkd_table)

# hkd_rows = hkd_table.findAll('tr')
# print(hkd_rows)


# Find the table element and extract the data
# rows = hkd_rows
# data = [['存款期', '定期存款年利率']]
# for row in rows:
#     cols = row.find_all('td')
#     cols = [col.text.strip() for col in cols]
#     data.append(cols)
#
#
# with open(f'{date}_HSBC.csv', mode='a', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['新資金'])
#     writer.writerows(data)



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
    rows = header.find_all('tr')
    # print(headers[0:5])


    for row in rows[1:]:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if len(cells) == 5:
            data.append(cells)


    with open(f'{date}_HSBC.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['定期存款'])
        writer.writerow([''])
        for row in data:
            if len(row) == 5:
                writer.writerow(row)


# new_fund()
# current_client()


