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


###### 新資金 ######
def new_fund():
    url = 'https://www.paob.com.hk/tc/retail-savings.html'

    session = requests_html.HTMLSession()

    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    hkd_table = soup.find('div', style='padding-left: 24px;').find('table', class_='table')

    # print(hkd_table)

    header = []
    thead = hkd_table.find('thead').find('tr')

    for th in thead.findAll('th'):
        th = th.text.strip()
        header.append(th)

    print(header)

    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    data = [header]
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)


    with open(f'{date}_ANT.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


new_fund()


