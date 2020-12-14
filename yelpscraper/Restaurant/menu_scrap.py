from requests import get
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import pymongo
import urllib.parse

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
menu_header_unstrip = column_div.find('h1').text
menu_header = menu_header_unstrip.strip()
print(menu_header)

menu_sections = soup.find('div',class_="menu-sections")
# print(menu-sections)
menu=[]
menu_item = menu_sections.findChildren(['h4'])
menu_item_price = menu_sections.findChildren(['li'])
for (h4, li) in zip(menu_item, menu_item_price):
    dataframe = {}
    item = h4.text
    dataframe['item-name'] = item.strip()
    price = li.text
    dataframe['item-price'] = price.strip()
    menu.append(dataframe)

# print(menu)
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz.menu
try:
    # db.insert_one(menu_header)
    db.insert_many(menu)
    print("Menu data inserted")
except:
    print("An error occured while storing menu data.")
