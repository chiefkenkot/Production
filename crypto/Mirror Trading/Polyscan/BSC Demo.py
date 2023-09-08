# ###### Login ######
#
# # steps:
# # 1. Scrap BSC Scan, whenever trade append, perform TG pop
# #     1.1 info = age (time), from, to
# #     1.2 TG poplib
# # 2. place order
#
# ###### Check BSC Scan ######
# # 1. how to identify new trades
# new_record = driver.find_element(By.XPATH, "//*[@id='transactions']/div[2]/table/tbody/tr[1]")
# age = driver.find_element(By.CLASS_NAME, "showAge ")
# print(age)
# # login_name.send_keys('ken_kot@chiefgroup.com.hk')
#
# time.sleep(1234)

##############################
import datetime
import requests_html
from bs4 import BeautifulSoup
from pprint import pprint
import time
from TG_Pop_Up import tg_pop
import schedule

session = requests_html.HTMLSession()

def scrap_data():

    # url = "https://bscscan.com/address/0x31eaf8923ea786baed08510ce21ac25e7b579982"
    url = "https://bscscan.com/address/0x24d671b2E1AF72864fd18cFcB77F094703Acf745"

    # Make a GET request to the URL
    # response = requests.get(url) # scarp page with Hardcode only
    response = session.get(url) # scarp page with Vairables

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")
    whole_table = soup.find('table', class_='table table-hover')

    # Find the desired information
    showAge = whole_table.find('td', class_='showAge')
    age_ago = showAge.find('span').text
    list_age_ago = list(age_ago)

    # print(list_age_ago)
    # time.sleep(1234)

    from_address = whole_table.find('span', class_='hash-tag text-truncate').text

    token = whole_table.find('a', class_='hash-tag text-truncate').text

    target_address = ('0x24d671b2E1AF72864fd18cFcB77F094703Acf745').lower()

    if list_age_ago[2] == 'm' and list_age_ago[0] <= '5':
        print(list_age_ago[2])
        print(list_age_ago[0])
        if from_address == target_address:
            print('address ok')
            if 'Pancake' in token:
                tg_pop()
        else:
            print('Wrong address')
    else:
        print('Waiting')


###### Production ######
while True:
    current_second = datetime.datetime.now().second
    if current_second == 0:
        scrap_data()
        print('waiting data')
        time.sleep(55)
