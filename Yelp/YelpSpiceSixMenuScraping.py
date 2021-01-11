# Nooras Fatima 
# https://github.com/nooras

#import
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs4
# from selenium import webdriver 
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import Chrome
import pandas as pd
import re
import requests
import urllib.parse

### Step 1 : Searching By Beautifulsoup By entering direct link
find = "Indian Food"
near = "Redando Beach, CA"
url = "https://www.yelp.com/search?find_desc=" + find + "&find_loc=" + near
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data,'html.parser')

### Step 2 : Finding Spice Six restaurant name By Beautifulsoup
spice_six = soup.find('a', text = re.compile('Spice Six'))

### Step 3 : Retrieving link and concatenate
url = "https://www.yelp.com" + spice_six['href']
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data,'html.parser')

### Step 4 : Converting link of menu page of Spice Six
url = url.split("?")[0]
url = url.replace("biz", "menu")
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data,'html.parser')

### Step 5 : Go to that link and retrieving data (Menu Name , Menu Price, categories)
# menu_name = []
# menu_price = []

# for j in soup.find_all('div', {"class":"menu-item"}):
#     menu_item_name = j.find('h4')
#     m = menu_item_name.text.strip()
#     menu_name.append(m)
#     menu_item_price = j.find('div',{"class":"menu-item-prices"})
#     p = menu_item_price.text.strip()
#     menu_price.append(p)

#Scraping all menu with categories
category_list = []
for j in soup.find_all('div', {"class":"section-header"}):
    category = j.find('h2')
    c = category.text.strip()
    c = c.replace(" ", "")
    if "(" in c:
        c = c.replace("(", "")
    if ")" in c:
        c = c.replace(")", "")
    category_list.append(c)
menu = {}   
count = 0
for j in soup.find_all('div', {"class":"u-space-b3"}): 
    menu_name = []
    menu_price = []
    for i in j.find_all('div', {"class":"menu-item"}):
        menu_item_name = i.find('h4')
        m = menu_item_name.text.strip()
        menu_name.append(m)
        menu_item_price = i.find('div',{"class":"menu-item-prices"})
        p = menu_item_price.text.strip()
        menu_price.append(p)
    data={'Menu_Name': menu_name, 'Menu_Prices': menu_price}
    df=pd.DataFrame(data=data)
    menu[category_list[count]] = df.to_dict("records")
    count += 1
    if count == len(category_list): 
        break
print("------------------------------------------------------")
print("Scraping Data")
print({"Restaurant Name": "Spice Six", "Restaurant Menu": menu})
print("------------------------------------------------------")

### Step 6 : Saving data in excel file
# data={'Menu Name': menu_name, 'Menu Prices': menu_price}
# df=pd.DataFrame(data=data)
# df.index+=1
# df.to_excel("yelp.xlsx")

### Inserting data into Monodb
import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz
restaurant = db.restaurantMenu
restaurant.insert_many([{"RestaurantName": "Spice Six", "RestaurantMenu": menu}]) #For inserting data 
r = restaurant.find({"RestaurantName": "Spice Six"})
for x in r:
    print(x)
