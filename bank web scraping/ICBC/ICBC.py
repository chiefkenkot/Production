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
    url = 'https://www.icbcasia.com/ICBC/%e6%b5%b7%e5%a4%96%e5%88%86%e8%a1%8c/%e5%b7%a5%e9%93%b6%e4%ba%9a%e6%b4%b2/TC/%e6%8a%95%e8%b3%87%e6%9c%8d%e5%8b%99/%e5%88%a9%e7%8e%87%e5%8f%8a%e5%8c%af%e7%8e%87%e6%9f%a5%e8%a9%a2/%e5%ad%98%e6%ac%be%e5%88%a9%e7%8e%87/default.htm'

    session = requests_html.HTMLSession()

    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    hkd_table = soup.find('table', class_='stylish-table ke-zeroborder')

    hkd_rows = hkd_table.findAll('tr')

    # Find the table element and extract the data
    rows = hkd_rows
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)


    with open(f'{date}_ICBC.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


new_fund()


