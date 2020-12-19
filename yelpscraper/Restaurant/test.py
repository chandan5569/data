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
response = get(url).text
soup = BeautifulSoup(response, 'html.parser')
# print(soup)

restaurantName = soup.find('h1')
restaurantName = restaurantName.text.strip()
restaurantName = restaurantName.strip("Menu for ")
print(restaurantName)

# category_list = []
# for j in soup.find_all('div',{"class":"section-header"}):
#     category = j.find('h2')
#     c = category.text.strip()
#     category_list.append(c)
# # print(category_list)

# menu = {}
# count = 0
# for j in soup.find_all('div', {"class": "u-space-b3"}):
#     menu_item = []
#     menu_item_price = []
#     for i in j.find_all('div', {"class": "menu-item"}):
#         menu_item_name = i.find('h4')
#         menu_item_name = menu_item_name.text.strip()
#         menu_item.append(menu_item_name)
#         item_price = i.find('div',{"class": "menu-item-prices"})
#         item_price = item_price.text.strip()
#         menu_item_price.append(item_price)

#     data = {'itemName': menu_item, 'itemPrice':menu_item_price}
#     df = pd.DataFrame(data=data)
#     menu[category_list[count]] = df.to_dict("records")
#     count += 1
#     if count == len(category_list):
#         break

# print(menu)


# column_div = soup.find('div',class_="column column-alpha")
# menu_header_unstrip = column_div.find('h1').text
# menu_header = menu_header_unstrip.strip()
# print(menu_header)

# menu_sections = soup.find('div',class_="menu-sections")
# # print(menu-sections)
# menu=[]
# menu_item = menu_sections.findChildren(['h4'])
# menu_item_price = menu_sections.findChildren(['li'])
# for (h4, li) in zip(menu_item, menu_item_price):
#     dataframe = {}
#     item = h4.text
#     dataframe['itemName'] = item.strip()
#     price = li.text
#     dataframe['itemPrice'] = price.strip()
#     menu.append(dataframe)

# print(menu)
# client = pymongo.MongoClient('mongodb+srv://shiraza:'+urllib.parse.quote_plus('Codemarket.123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
# db = client.codemarket_shiraz.menu_data
# try:
#     # db.insert_one(menu_header)
#     db.insert_many(menu)
#     print("Menu data inserted")
# except:
#     print("An error occured while storing menu data.")
