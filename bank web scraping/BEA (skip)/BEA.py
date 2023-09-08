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
def existing_fund():
    url = 'https://www.hkbea.com/cgi-bin/rate_hkddr.jsp?language=tc&language=tc'

    session = requests_html.HTMLSession()

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    hkd_table = soup.find('table', class_='table3')

    # header = []
    # thead = hkd_table.findAll('th')
    #
    # for th in thead:
    #     th = th.text.strip()
    #     header.append(th)

    # print(header)

    hkd_rows = hkd_table.findAll('tr')
    td = hkd_table.findAll('td', class_='alignR')

    # Find the table element and extract the data
    rows = hkd_rows
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        # print(cols)
        if len(cols) == 6:
            cols.insert(0, '金額')
            data.append(cols)
        # if len(cols) == 8:
        #     cols.pop(0)
        #     data.append(cols)
        else:
            pass

    cell = [td.text.strip() for td in td]
    cell = [cell[i:i+7] for i in range(0, len(cell), 7)]

    for i in cell:
        data.append(i)



    with open(f'{date}_BEA.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


existing_fund()


