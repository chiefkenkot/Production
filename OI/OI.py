import requests
import pandas as pd
import numpy as np
import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

unix_time = str(int(time.time() *1000))
# print(unix_time)

###### Merge old OI and BTC to same dataframe ######
# url = f'https://live-api.cryptoquant.com/api/v3/charts/61adc2916bc0e955292d727b?window=DAY&from=1051718400000&to={unix_time}&limit=70000'
#
# driver = webdriver.Chrome()
# driver.get(url)
# driver.implicitly_wait(10)
# content = driver.page_source
#
# soup = BeautifulSoup(content, 'html.parser')
#
# data = soup.find(style='word-wrap: break-word; white-space: pre-wrap;').text
#
# data = json.loads(data)['result']['data']
#
# df = pd.DataFrame(data, columns=['unix time', 'oi'])
#
# # print(df)
#
# # driver.quit()
#
#
# url2 = f'https://live-api.cryptoquant.com/api/v2/assets/61712eb35a176168a02409e8/price?window=DAY&from=1051718400000&to={unix_time}&limit=70000'
#
# driver = webdriver.Chrome()
# driver.get(url2)
# driver.implicitly_wait(10)
# content = driver.page_source
#
# soup = BeautifulSoup(content, 'html.parser')
#
# data2 = soup.find(style='word-wrap: break-word; white-space: pre-wrap;').text
#
# data2 = json.loads(data2)['data']
#
# df2 = pd.DataFrame(data2, columns=['unix time', 'BTC price'])
#
# # print(df2)
#
# driver.quit()
#
# df3 = pd.DataFrame.merge(df2, df, on='unix time')
# df3 = df3.rename(columns= {'unix time':'date'})
# df3['date'] = pd.to_datetime(df3['date'], unit='ms')
#
# # df3.to_csv('BTC OI Data.CSV', index=False)
# print(df3)


###### Now Price ######

# now_price_url = 'https://live-api.cryptoquant.com/api/v2/assets/61712eb35a176168a02409e8/now-price'
#
# driver = webdriver.Chrome()
# driver.get(now_price_url)
# driver.implicitly_wait(10)
# content = driver.page_source
#
# soup = BeautifulSoup(content, 'html.parser')
#
# now_price = json.loads(soup.text)['price']
#
# print(now_price)
# # 27786.98590166


# new_oi_url = 'https://cryptoquant.com/asset/btc/chart/derivatives/open-interest?exchange=all_exchange&symbol=all_symbol&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line'
#
# driver = webdriver.Chrome()
# driver.get(new_oi_url)
# driver.implicitly_wait(10)
# content = driver.page_source
#
# soup = BeautifulSoup(content, 'html.parser')
#
# oi = json.loads(soup)
#
# print(oi)

url = "https://cryptoquant.com/asset/btc/chart/derivatives/open-interest?exchange=all_exchange&symbol=all_symbol&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line"

driver = webdriver.Chrome()
driver.get(url)
# driver.implicitly_wait(10)
#
# content = driver.page_source
#
# soup = BeautifulSoup(content, 'html.parser')
# # soup = json.loads(soup.text)
#
# # last_value_div = soup.find("div", class_="detail-content").find('div', class_='last').text
# last_value_div = soup.find("div", class_="detail-content").contents
#
#
# print(last_value_div)
# # pprint(soup)


# Wait for the chart container to be visible
wait = WebDriverWait(driver, 30)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.highcharts-container")))

# Try to fetch chart data from the window object
chart_data = driver.execute_script("""
    for (var key in window) {
        if (window.hasOwnProperty(key) && window[key] && window[key].chart && window[key].chart.series) {
            return JSON.stringify(window[key].chart.series[0].options.data);
        }
    }
    return null;
""")

if chart_data is None:
    print("Error: Chart data not found.")
    driver.quit()
    exit(1)

# Parse the chart data and get the last value
data_points = json.loads(chart_data)
last_value = data_points[-1]['y']

print("Last value:", last_value)

driver.quit()

# Extract the numeric value
# last_value = float(re.search(r'\d+[\.,]?\d*', last_value_text).group().replace(',', ''))
#
# print("Last value:", last_value)

driver.quit()


# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "detail-content"))
#     )
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     last_value_div = soup.find("div", class_="last is-show")
#
#     if last_value_div:
#         last_value = last_value_div.text.strip()
#         print("Last Value:", last_value)
#     else:
#         print("Target <div> not found")
# finally:
#     driver.quit()

