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
import sys
import pymongo
from bson.objectid import ObjectId

#Db Coonection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz
restaurant = db.restaurantMenu

### Step 1 : Searching By Beautifulsoup By entering direct link
IdUser = sys.argv[1]
# find = "Indian Food"
find = sys.argv[2]
# near = "Redando Beach, CA"
near = sys.argv[3]

url = "https://www.yelp.com/search?find_desc=" + find + "&find_loc=" + near
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data,'html.parser')

### Step 2 : Finding Spice Six restaurant name By Beautifulsoup
rest_name = 'Famous Tandoori'
rest_name2 = str(sys.argv[4])
print("RestName", rest_name, type(rest_name), rest_name2, type(rest_name2))
restATag = soup.find('a', string=rest_name)
restATag2 = soup.find('a', string=rest_name2)
print(restATag)
print("-------")
print(restATag2)

### Step 3 : Retrieving link and concatenate
url = "https://www.yelp.com" + restATag['href']
#print("URLLLLL", url)
response = requests.get(url)
data = response.text
#print(data)
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
allMenu = []
count = 0
for j in soup.find_all('div', {"class":"u-space-b3"}): 
    menu = {}   
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
    menu["Category"] = category_list[count]
    menu["AllItems"] = df.to_dict("records")
    allMenu.append(menu)
    count += 1
    if count == len(category_list): 
        break
print("------------------------------------------------------")
print("Scraping Data")
print({"IdUser" : IdUser, "FindKeyWord" : find, "Location": near, "RestaurantName": rest_name, "RestaurantMenu": allMenu})
print("------------------------------------------------------")

### Step 6 : Saving data in excel file
# data={'Menu Name': menu_name, 'Menu Prices': menu_price}
# df=pd.DataFrame(data=data)
# df.index+=1
# df.to_excel("yelp.xlsx")

### Inserting data into Monodb

# l = list(restaurant.find({"IdUser": "nf", "FindKeyWord" : "Indian Food", "Location" : "Redondo Beach, CA", "RestaurantName" : "Spice Six"}))
l = list(restaurant.find({"RestaurantName" : rest_name })) #Fetching
if not l:  # if l is empty means no data found of restaurantName
    restaurant.insert([{"IdUser" : IdUser, "FindKeyWord" : find, "Location": near, "RestaurantName": rest_name, "RestaurantMenu": allMenu}]) #For inserting data
    print("Menu Inserted Successfully")
else: # Update or Chcek already prent or not
    restMenu = l[0]['RestaurantMenu']
    Flag = 0
    listFetchMenu = []
    for x in restMenu:
        if x is not None:
            listFetchMenu.append(x['Category'])
    listAllMenu = []
    for x in allMenu:
        if x is not None:
            listAllMenu.append(x['Category'])
    for x in listAllMenu:
        if x not in listFetchMenu:
            Flag = 1
            restaurant.update_one({'_id':l[0]['_id']}, {"$set": {"RestaurantMenu": allMenu}})
            print("Menu Updated.")
            break
    if Flag == 0:
        print("Menu is already Present.")
    else:
        print("Menu Updated Successfully.")
r = restaurant.find({"RestaurantName": rest_name})
for x in r:
    print(x)
