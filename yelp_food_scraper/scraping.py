#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection


# In[43]:


get_ipython().system('pip install mongoengine')


# In[5]:


client = pymongo.MongoClient('mongodb+srv://bilalm:'+urllib.parse.quote_plus('Codemarket.123')+'@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
my_db = client['dreamjobpal']
db = my_db.hotel_menu


# In[7]:


def hotel_menu():
    item = input("Please enter the name of food item:")
    place = input("Please enter the location:")
    
    client = pymongo.MongoClient('mongodb+srv://bilalm:'+urllib.parse.quote_plus('Codemarket.123')+'@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.hotel_menu
    
    data = []
    for page in range (0, 10, 10):
        source = requests.get(f"https://www.yelp.com/search?find_desc={item}&find_loc={place}&ns=1&start={page}").text
        soup = BeautifulSoup(source, 'html.parser')

        for i in soup.findAll("a", {"class": "link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"}):         
            if 'ad_business_id' not in i['href']:

                link = "https://www.yelp.com/"+i['href']
                menu_link = link.split('/')
                menu_link[4] = '/menu/'
                menu_link[1] = '//'
                menu_link = ''.join(menu_link)
                menu_page = menu_link 
                print(link)
                print("Hotel menu- " +menu_page)
                menu_url = requests.get(menu_link)
                menu_soup = BeautifulSoup(menu_url.content, 'lxml')
                hotel_soup  = BeautifulSoup(menu_url.content, 'lxml')
                hotel_name = hotel_soup.find('h1')
                if hotel_name is None:
                    continue 
                hotel_name = hotel_name.text.strip()
                #print(hotel_name)
                menu = menu_soup.find_all("div", {"class": "menu-item"})
                for m in menu:
                    name_result=m.find('h4').text.strip()
                    price_result = m.find('li', {"class": "menu-item-price-amount"})
                    if price_result is None:
                        container = m.find("div", {"class": "menu-item-prices arrange_unit"})
                        price_result = container.findAll('tr')
                        l1=[]
                        for price in price_result:
                            size = price.find('th').text.strip()
                            price = price.find('td').text.strip()
                            l1.append(size + ' - ' + price)
                            price_result = ' , '.join(l1)
                    else:
                        price_result=price_result.text.strip()
                    data.append({"hotel":hotel_name,"item":name_result,"price":price_result})
                    db.insert({"hotel":hotel_name,"item":name_result,"price":price_result})
    print(data)
    dataset = pd.DataFrame(data)
    dataset.to_csv(item+'.csv')


# In[8]:


hotel_menu()

