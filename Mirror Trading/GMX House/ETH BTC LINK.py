import time

import requests
import requests_html
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.gmx.house/arbitrum/account/0xfad9ec895839fbd65f9574101a56895b2059acc2'

###### Send Request #######
session = requests_html.HTMLSession()
driver = webdriver.Chrome()
soup_response = requests.get(url)
response = driver.get(url)

time.sleep(5)

soup = BeautifulSoup(soup_response.text, 'html.parser')
table = soup.find('column', class_='•15')


print(soup)