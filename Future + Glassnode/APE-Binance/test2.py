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

import requests_html
from bs4 import BeautifulSoup
from pprint import pprint
import time

session = requests_html.HTMLSession()

url = "https://bscscan.com/address/0x31eaf8923ea786baed08510ce21ac25e7b579982"

# Make a GET request to the URL
# response = requests.get(url) # scarp page with Hardcode only
response = session.get(url) # scarp page with Vairables

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, "html.parser")

whole_table = soup.find('table', class_='table table-hover')


# Find the desired information
def age():
    showAge = whole_table.find('td', class_='showAge')
    age_ago = showAge.find('span').text
    return age_ago


from_address = whole_table.find('span', class_='hash-tag text-truncate').text

def to_info():
    to = whole_table.find('a', class_='hash-tag text-truncate').text


age()
# from_info()
to_info()

if age() <= '5 mins':
    if from_address == '0x31eaf8923ea786baed08510ce21ac25e7b579982':
        print('from info correct')

    else:
        print('from info incorrect')

else:
    print('waiting')
time.sleep(1234)




token_name = soup.find(id="ContentPlaceHolder1_divSummary")
if token_name:
    token_name = token_name.text.strip()
else:
    token_name = "Information not available"

token_symbol = soup.find("div", class_="token-symbol")
if token_symbol:
    token_symbol = token_symbol.text.strip()
else:
    token_symbol = "Information not available"

token_price = soup.find("div", class_="token-price")
if token_price:
    token_price = token_price.text.strip()
else:
    token_price = "Information not available"

# Print the results
print("Token Name:", token_name)
print("Token Symbol:", token_symbol)
print("Token Price:", token_price)


