import datetime
import time
from requests_html import HTMLSession

import requests_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def fuc_tg_pop(message):
    base_url = 'https://api.telegram.org/bot5688971254:AAF_HIUKntnxAHdV34ge3Aegike8xiQbHmU/sendMessage?chat_id=-1001959557289&text='

    requests.get(base_url + message)


def tg_pop(message):
    base_url = 'https://api.telegram.org/bot5366919147:AAHXp_HHe2o38FBiahz8PspWah6IYHOXbJ8/sendMessage?chat_id=-861322443&text='

    # message = ('HHYP just buy BUSD')

    requests.get(base_url + message)


while True:
    # try:
        address_list = {'項目方地址1': '0x755912C2247Ec134a65D7c62275E16980B95C7d5',
                        '項目方地址2': '0xBAa7febF8288AE068C9766a7036F1d4788FAB1BF',
                        '項目方地址3': '0xb08f16A673AeC5987582F6143118fA33FaF16442',
                        'Walker': '0x4Bb028899148478dC578522Ca4e56eC282daC14f',
                        'You Hao': '0xD3AB5Cf3Ec86052087182D3F0b44AF3e87C569e9',
                        '大波段哥1': '0x2fe25d626377a0b3e43a6cb4fc06aaf114b0a39a',
                        '大波段哥2': '0x5dbc81277f8b1254bb4f27491735514ac976d618',
                        'JC': '0x8fea8b3bb899791dbcc937c5ded9d12b32cd0bd9',
                        'Tbag Cracy': '0xd951a9edacf3a791987c224f743084de1aca7183',
                        '真波段哥': '0xe0b5a76633a6f249Ae57C8386EDB994B2d119774',
                        '糖果生意 Admin': '0xCe345b71Dac5dCE503b9Db9CB58Ba4fA35158Eb2',
                        '面大地址': '0xACd5844DCefC76220c69912Ba5e856d43065b821',
                        'Strong buy guy': '0x9b84CdEf27Efdd7F971ceae75d9D748f7Dc08b24',
                        'Rich investor': '0x094034D3aDb20D35b98314FEdA16e0545535c526',
                        'Mr Stone3': '0xbF9a53043D8AF9548593dea3BDA319755EcAFc88',
                        'self': '0x24d671b2E1AF72864fd18cFcB77F094703Acf745'}

        for key, value in address_list.items():
            url = f'https://app.zerion.io/tokens/FUC-51866158-d970-49a4-91ef-c7643a1b6892?address={value}'

            session = HTMLSession()
            content = session.get(url)
            for _ in range(3):  # Retry up to 3 times
                content.html.render()
                time.sleep(3)
                soup = BeautifulSoup(content.html.html, "html.parser")

                table = soup.find('div', class_='VStack-sc-1vdo21d-0 cnxWvB')
                if table:
                    break
                time.sleep(5)  # Wait for 5 seconds before trying again

            if not table:
                print(f"Failed to find the required element for {key}")
                continue

            table2 = table.find('div', class_='VStack-sc-1vdo21d-0 cnxWzk')

            action = table.find('div', class_='UIText-sc-96tl0y-0 efmSIO').text
            date = table.find('div', class_='UIText-sc-96tl0y-0 dBQSjA').text
            token = table2.find('div', kind='subtitle/m_reg').text
            usdt = table2.find('div', class_='UIText-sc-96tl0y-0 dBQSjA').text

            # print(table.text)
            # print(action)
            # print(date)
            print(token)
            # print(usdt)
            current_date = datetime.datetime.now()
            # current_date = "2023-06-03 10:22:53.049035"

            # date_1 = datetime.datetime.strptime(date, "%Y年%m月%d日 %H:%M")
            date_1 = datetime.datetime.strptime(date, "%b %d, %Y, %I:%M %p")
            # date_2 = datetime.datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S.%f")
            time_difference = current_date - date_1
            # time_difference = date_2 - date_1
            # print(time_difference)

            message = (f'''{key} has movement

{date} (UTC)
{action}
Action: {token} / {usdt} 

{url}''')

            # if datetime.timedelta(minutes=-5) <= time_difference <= datetime.timedelta(minutes=5):
            if datetime.timedelta(minutes=0) <= time_difference <= datetime.timedelta(minutes=5):
                fuc_tg_pop(message)
            else:
                print(f'{key} last action was {time_difference} ago')

            # driver.quit()
            time.sleep(1)
    # except:
    #     message = 'FUC鯨 error occurs'
    #     print(message)
    #     tg_pop(message)
    #     continue







