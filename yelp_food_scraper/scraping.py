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


# In[59]:


def hotel_menu():
    item = input("Please enter the name of food item: ")
    place = input("Please enter the location: ")
    number_of_hotels = int(input("Enter the number of hotels: "))
    count = 0
    
    client = pymongo.MongoClient('mongodb+srv://bilalm:'+urllib.parse.quote_plus('Codemarket.123')+'@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.hotel_menu
    
    data = []
    
    for page in range (0, 240, 10):
        if count >= number_of_hotels:
            break
        source = requests.get(f"https://www.yelp.com/search?find_desc={item}&find_loc={place}&ns=1&start={page}").text
        soup = BeautifulSoup(source, 'html.parser')
        

        for i in soup.findAll("a", {"class": "link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"}):         
            
            if count >= number_of_hotels:
                break
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
                menu = menu_soup.find("div", {"class": "menu-sections"})
                h2 = menu.find_all("h2")
                
                for h in h2:
                    section = h.text.strip()
                    items = h.parent.find_next_sibling()
                    h4 = items.find_all("h4")
                    
                    for h44 in h4:
                        name_result=h44.text.strip()
                        price =h44.parent.find_next_sibling()
                        price_result = price.find("li", {"class", "menu-item-price-amount"})
                        
                        if price_result is None:
                            price_result = price.findAll('tr')#container.findAll('tr')
                            l1=[]
                            
                            for p in price_result:
                                size = p.find('th').text.strip()
                                pr = p.find('td').text.strip()
                                l1.append(size + ' - ' + pr)
                                price_result = ' , '.join(l1)
                        else:
                            price_result=price_result.text.strip()
                        
                        if len(price_result) == 0:
                            price_result = ""
                        
                        data.append({"Restaurant":hotel_name, "Category":section, "Item":name_result,"Price":price_result})
                       # print({"Hotel":hotel_name, "category":section, "item":name_result,"price":price_result})
                        db.insert({"Restaurant":hotel_name, "Category":section, "Item":name_result,"Price":price_result})
                count +=1
                
                
           
   # print(data)
    dataset = pd.DataFrame(data,columns=['Restaurant', 'Category', 'Item', 'Price'])
    dataset.to_csv(item+'.csv')


# In[60]:


hotel_menu()


# In[ ]:





# In[ ]:





# In[ ]:




