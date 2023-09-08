import datetime
from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


url = 'https://debank.com/profile/0x2676b2fb25ee10c2cc2514ab4705add24a1f33c3/history?chain=eth&token='

while True:

    # Set up the Selenium webdriver
    options = Options()
    # options.add_argument('--headless')
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    ###### Wait until page loaded ######
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[3]/div/div[2]')))
    time.sleep(10)

    ###### Scrap Content ######
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('div', class_='History_table__9zhFG')
    table_info = table.text
    row = table.find('div', class_='History_tableLine__3dtlF')
    row_info = row.text

    # print(row_info)
    # time.sleep(1234)

    ###### trade time ######
    trade_time = row.find('div', class_='History_sinceTime__3JN2E').text
    # trade_time = '2023/03/05 11:25:35'
    trade_time_datetime_object = datetime.datetime.strptime(trade_time, '%Y/%m/%d %H:%M:%S') # convert to datetime object
    time_now = (datetime.datetime.now())
    # converted_time = time_now.strftime('%Y/%m/%d %H:%M:%S') # convert datetime object to str

    ###### trade info ######
    trade = row.find('div', class_='History_tokenChangeWrap__K9hqy')
    trade_info = trade.text

    ###### Time Diff Calculation ######
    time_diff = time_now - trade_time_datetime_object
    time_diff_minutes = time_diff.total_seconds()/60

    ###### TG Pop ######
    def tg_pop():
        base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='
        message = ('ETH-stupid-money:') + str(' ' + trade_time + '_' + trade_info + ' ' + 'https://debank.com/profile/0x2676b2fb25ee10c2cc2514ab4705add24a1f33c3/history?chain=eth&token=')
        requests.get(base_url + message)

    # print(row_info)
    # print(trade_time)
    # print(trade_info)
    print(time_now)
    # print(time_diff)
    # print(time_diff_minutes)


    if time_diff_minutes <= 5:
        tg_pop()

    else:
        print('No New Trade')


    # Close the webdriver
    driver.quit()

    time.sleep(300)
    # time.sleep(30)