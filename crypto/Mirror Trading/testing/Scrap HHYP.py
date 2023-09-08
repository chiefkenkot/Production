import datetime
import requests_html
from bs4 import BeautifulSoup
from pprint import pprint
import time
from TG_Pop_Up import tg_pop
import schedule
from pybit import usdt_perpetual
import pal

###### Exchange Order ######
session_auth = usdt_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key=pal.api_key,
    api_secret=pal.api_secret
)

def open_long():
    session_auth.place_active_order(
        symbol="USDCUSDT",
        side="Buy",
        order_type="Market",
        qty=0.5,
        # price=5,
        time_in_force="GoodTillCancel",
        reduce_only=False,
        close_on_trigger=False,
        position_idx=0
    )

session = requests_html.HTMLSession()

def scrap_data():

    url = "https://bscscan.com/address/0x31eaf8923ea786baed08510ce21ac25e7b579982"
    # url = "https://bscscan.com/address/0x24d671b2E1AF72864fd18cFcB77F094703Acf745"

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

    print(whole_table)
    time.sleep(1234)

    from_address = whole_table.find('span', class_='hash-tag text-truncate').text

    token = whole_table.find('a', class_='hash-tag text-truncate').text

    target_address = ('0x31eaf8923ea786baed08510ce21ac25e7b579982').lower() # variable

    if list_age_ago[2] == 'm' and list_age_ago[0] <= '5':
        print(list_age_ago[2])
        print(list_age_ago[0])
        if from_address == target_address:
            print('address ok')
            if 'BUSD' in token: # variable
                open_long()
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
        time.sleep(290)
