import time
import requests
from pybit import spot
from pprint import pprint


###### Trade History ######


###### TG POP ######

base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

message = str(buy_record)

requests.get(base_url+message)


