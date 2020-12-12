from requests import get
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
driver = webdriver.Chrome('/home/dhruv034/Desktop/codemarket/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
#driver = webdriver.Chrome('E:/Codes/chromedriver.exe')#,chrome_options=chrome_options)

url = "https://www.yelp.com/menu/indias-tandoori-los-angeles"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

column_div = soup.find('div',class_="column column-alpha")
menu_header = column_div.find('h1').text
print(menu_header)

menu_sections = soup.find('div',class_="menu-sections")
# print(menu-sections)

# section_header = menu_sections.findChildren(['h2'])
# for h2 in section_header:
#     print(h2.text)
item_list = list()
price_list = list()

menu_item = menu_sections.findChildren(['h4'])
for h4 in menu_item:
    item = h4.text
    item_list.append(item.strip())

menu_item_price = menu_sections.findChildren(['li'])
for li in menu_item_price:
    price = li.text
    price_list.append(price.strip())

menu = zip(item_list,price_list)
print(dict(menu))
