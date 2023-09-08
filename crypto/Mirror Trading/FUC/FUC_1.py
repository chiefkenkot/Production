import time
from selenium import webdriver
from pprint import pprint
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://arbiscan.io/address-tokenpage?m=normal&a=0xACd5844DCefC76220c69912Ba5e856d43065b821"

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
content = driver.page_source

# response = requests.get(url)
soup = BeautifulSoup(content, "html.parser")

# print(soup)

table = soup.find('table', class_='table table-hover').find('tbody').find('tr')
# table = soup.find('table', class_='table table-hover').find('tbody').find_all('tr')
age = table.find('td', class_='showAge').text

list = []

for i in table:
    td = i.text.strip()
    print(td)
    list.append(td)

age = list[3]
age_min = age[3]
age_num = age[0]

if age_min == 'm':
    if age_num <= '5':
        print(age)
    else:
        print('age num wrong')
else:
    print('no')

print(age)


# if age < 4




# Find the table containing the transactions
# transaction_table = soup.find("div", {"class": "table-responsive"})

# # Extract the header row to get the column names
# header_row = transaction_table.find("thead").find_all("th")
# headers = [header.text.strip() for header in header_row]
#
# # Extract the data rows
# data_rows = transaction_table.find("tbody").find_all("tr")
#
# # print(type(data_rows))
# print(data_rows)


# transactions = []
#
# for row in data_rows:
#     cells = row.find_all("td")
#     transaction_data = {}
#     if len(cells) == len(headers):  # Check if the number of cells matches the number of headers
#         for i, cell in enumerate(cells):
#             # Use the header text as a key and store the cell text as the value
#             transaction_data[headers[i]] = cell.text.strip()
#         transactions.append(transaction_data)
#
# for transaction in transactions:
#     print(transaction)

# <class 'bs4.element.ResultSet'>
# [<tr><td><a class="js-txnAdditional-1 btn btn-xs btn-icon btn-soft-secondary myFnExpandBox" role="button" tabindex="0" type="button"><i class="far fa-eye btn-icon__inner"></i></a></td><td><a class="hash-tag text-truncate myFnExpandBox_searchVal" href="/tx/0xb7e4f5fa81589dee0e3b01fa7405d82f9de8788a17175cf5c857431a88d112b0">0xb7e4f5fa81589dee0e3b01fa7405d82f9de8788a17175cf5c857431a88d112b0</a></td><td><span class="u-label u-label--xs u-label--info rounded text-dark text-center" data-boundary="viewport" data-html="true" data-original-title="Execute" data-toggle="tooltip" style="min-width:68px;" title="">Execute</span></td><td class="d-none d-sm-table-cell"><a href="/block/90621040">90621040</a></td><td class="showDate" style="display:none !important"><span data-original-title="54 mins ago" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">2023-05-14 13:24:37</span></td><td class="showAge" style=""><span data-original-title="2023-05-14 13:24:37" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">54 mins ago</span></td><td><span class="hash-tag text-truncate" data-original-title="0xa05bd52f630106c4a154d5402d7df04832f2d1eb" data-placement="bottom" data-toggle="tooltip" title="">0xa05bd52f630106c4a154d5402d7df04832f2d1eb</span></td><td><span class="u-label u-label--xs u-label--warning color-strong text-uppercase text-center w-100 rounded text-nowrap">OUT</span></td><td><span style="white-space: nowrap;"><i class="far fa-file-alt text-secondary" data-original-title="Contract" data-placement="bottom" data-toggle="tooltip" title=""></i> <a class="hash-tag text-truncate" data-boundary="viewport" data-html="true" data-original-title="Uniswap: Universal Router
# (0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5)" data-placement="bottom" data-toggle="tooltip" href="/address/0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5" title="">Uniswap: Universal Router</a></span></td><td>0 ETH</td><td class="showTxnFee" style=""><span class="small text-secondary">0<b>.</b>00017937</span></td><td class="showGasPrice" style="display:none !important; "><span class="small text-secondary">0<b>.</b>1</span></td></tr>, <tr><td><a class="js-txnAdditional-1 btn btn-xs btn-icon btn-soft-secondary myFnExpandBox" role="button" tabindex="0" type="button"><i class="far fa-eye btn-icon__inner"></i></a></td><td><a class="hash-tag text-truncate myFnExpandBox_searchVal" href="/tx/0x5717817570abfcea6dd42dfbf1798f86f34e89b9260fa0cf2bc391baf918e22a">0x5717817570abfcea6dd42dfbf1798f86f34e89b9260fa0cf2bc391baf918e22a</a></td><td><span class="u-label u-label--xs u-label--info rounded text-dark text-center" data-boundary="viewport" data-html="true" data-original-title="Execute" data-toggle="tooltip" style="min-width:68px;" title="">Execute</span></td><td class="d-none d-sm-table-cell"><a href="/block/90499453">90499453</a></td><td class="showDate" style="display:none !important"><span data-original-title="9 hrs 25 mins ago" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">2023-05-14 4:53:41</span></td><td class="showAge" style=""><span data-original-title="2023-05-14 4:53:41" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">9 hrs 25 mins ago</span></td><td><span class="hash-tag text-truncate" data-original-title="0xa05bd52f630106c4a154d5402d7df04832f2d1eb" data-placement="bottom" data-toggle="tooltip" title="">0xa05bd52f630106c4a154d5402d7df04832f2d1eb</span></td><td><span class="u-label u-label--xs u-label--warning color-strong text-uppercase text-center w-100 rounded text-nowrap">OUT</span></td><td><span style="white-space: nowrap;"><i class="far fa-file-alt text-secondary" data-original-title="Contract" data-placement="bottom" data-toggle="tooltip" title=""></i> <a class="hash-tag text-truncate" data-boundary="viewport" data-html="true" data-original-title="Uniswap: Universal Router
# (0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5)" data-placement="bottom" data-toggle="tooltip" href="/address/0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5" title="">Uniswap: Universal Router</a></span></td><td>0 ETH</td><td class="showTxnFee" style=""><span class="small text-secondary">0<b>.</b>00015657</span></td><td class="showGasPrice" style="display:none !important; "><span class="small text-secondary">0<b>.</b>1</span></td></tr>, <tr><td><a class="js-txnAdditional-1 btn btn-xs btn-icon btn-soft-secondary myFnExpandBox" role="button" tabindex="0" type="button"><i class="far fa-eye btn-icon__inner"></i></a></td><td><a class="hash-tag text-truncate myFnExpandBox_searchVal" href="/tx/0x2bb9168b74b3a00e3616191ed29dff650dcde70c40f2deb58234bbf1b713b587">0x2bb9168b74b3a00e3616191ed29dff650dcde70c40f2deb58234bbf1b713b587</a></td><td><span class="u-label u-label--xs u-label--info rounded text-dark text-center" data-boundary="viewport" data-html="true" data-original-title="Execute" data-toggle="tooltip" style="min-width:68px;" title="">Execute</span></td><td class="d-none d-sm-table-cell"><a href="/block/90493437">90493437</a></td><td class="showDate" style="display:none !important"><span data-original-title="9 hrs 51 mins ago" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">2023-05-14 4:27:39</span></td><td class="showAge" style=""><span data-original-title="2023-05-14 4:27:39" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">9 hrs 51 mins ago</span></td><td><span class="hash-tag text-truncate" data-original-title="0xa05bd52f630106c4a154d5402d7df04832f2d1eb" data-placement="bottom" data-toggle="tooltip" title="">0xa05bd52f630106c4a154d5402d7df04832f2d1eb</span></td><td><span class="u-label u-label--xs u-label--warning color-strong text-uppercase text-center w-100 rounded text-nowrap">OUT</span></td><td><span style="white-space: nowrap;"><i class="far fa-file-alt text-secondary" data-original-title="Contract" data-placement="bottom" data-toggle="tooltip" title=""></i> <a class="hash-tag text-truncate" data-boundary="viewport" data-html="true" data-original-title="Uniswap: Universal Router
# (0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5)" data-placement="bottom" data-toggle="tooltip" href="/address/0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5" title="">Uniswap: Universal Router</a></span></td><td>0 ETH</td><td class="showTxnFee" style=""><span class="small text-secondary">0<b>.</b>00015837</span></td><td class="showGasPrice" style="display:none !important; "><span class="small text-secondary">0<b>.</b>1</span></td></tr>, <tr><td><a class="js-txnAdditional-1 btn btn-xs btn-icon btn-soft-secondary myFnExpandBox" role="button" tabindex="0" type="button"><i class="far fa-eye btn-icon__inner"></i></a></td><td><a class="hash-tag text-truncate myFnExpandBox_searchVal" href="/tx/0xea46edc73a8e859bb10dfff56413c608f9208845c3b41e2c25a4923c016aca57">0xea46edc73a8e859bb10dfff56413c608f9208845c3b41e2c25a4923c016aca57</a></td><td><span class="u-label u-label--xs u-label--info rounded text-dark text-center" data-boundary="viewport" data-html="true" data-original-title="Execute" data-toggle="tooltip" style="min-width:68px;" title="">Execute</span></td><td class="d-none d-sm-table-cell"><a href="/block/90243632">90243632</a></td><td class="showDate" style="display:none !important"><span data-original-title="1 day 3 hrs ago" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">2023-05-13 10:22:38</span></td><td class="showAge" style=""><span data-original-title="2023-05-13 10:22:38" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">1 day 3 hrs ago</span></td><td><span class="hash-tag text-truncate" data-original-title="0xa05bd52f630106c4a154d5402d7df04832f2d1eb" data-placement="bottom" data-toggle="tooltip" title="">0xa05bd52f630106c4a154d5402d7df04832f2d1eb</span></td><td><span class="u-label u-label--xs u-label--warning color-strong text-uppercase text-center w-100 rounded text-nowrap">OUT</span></td><td><span style="white-space: nowrap;"><i class="far fa-file-alt text-secondary" data-original-title="Contract" data-placement="bottom" data-toggle="tooltip" title=""></i> <a class="hash-tag text-truncate" data-boundary="viewport" data-html="true" data-original-title="Uniswap: Universal Router
# (0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5)" data-placement="bottom" data-toggle="tooltip" href="/address/0x4c60051384bd2d3c01bfc845cf5f4b44bcbe9de5" title="">Uniswap: Universal Router</a></span></td><td>0 ETH</td><td class="showTxnFee" style=""><span class="small text-secondary">0<b>.</b>00017281</span></td><td class="showGasPrice" style="display:none !important; "><span class="small text-secondary">0<b>.</b>1</span></td></tr>, <tr><td><a class="js-txnAdditional-1 btn btn-xs btn-icon btn-soft-secondary myFnExpandBox" role="button" tabindex="0" type="button"><i class="far fa-eye btn-icon__inner"></i></a></td><td><a class="hash-tag text-truncate myFnExpandBox_searchVal" href="/tx/0x102620363c1518ffd1159c92f9221b807b4af6fcf1427547f952b377381c9df3">0x102620363c1518ffd1159c92f9221b807b4af6fcf1427547f952b377381c9df3</a></td><td><span class="u-label u-label--xs u-label--info rounded text-dark text-center" data-boundary="viewport" data-html="true" data-original-title="Execute" data-toggle="tooltip" style="min-width:68px;" title="">Execute</span></td><td class="d-none d-sm-table-cell"><a href="/block/90116353">90116353</a></td><td class="showDate" style="display:none !important"><span data-original-title="1 day 12 hrs ago" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">2023-05-13 1:21:11</span></td><td class="showAge" style=""><span data-original-title="2023-05-13 1:21:11" data-placement="bottom" data-toggle="tooltip" rel="tooltip" title="">1 day 12 hrs ago</span></td><td><span class="hash-tag text-truncate" data-original-title="0xa05bd52f630106c4a154d5402d7df04832f2d1eb" data-placement="bottom" data-toggle="tooltip" title="">0xa05bd52f630106c4a154d5402d7df04832f2d1eb</span></td><td><span class="u-label u-label--xs u-label--warning color-strong text-uppercase text-center w-100 rounded text-nowrap">OUT</span></td><td><span style="white-space: nowrap;"><i class="far fa-file-alt text-secondary" data-original-title="Contract" data-placement="bottom" data-toggle="tooltip" title=""></i> <a class="hash-tag text-truncate" data-boundary="viewport" data-html="true" data-original-title="Uniswap: Universal Router
