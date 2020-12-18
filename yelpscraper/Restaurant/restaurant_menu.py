from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import urllib.parse
import dns
import argparse
from mongoengine import *
from mongoengine.context_managers import switch_collection

def restaurant_menu():
    item = "Indian Food"
    place = "Redondo Beach"
    data = []
    for start in range (0, 10, 10):
        source = requests.get(f"https://www.yelp.com/search?find_desc={item}&find_loc={place}&ns=1&start={start}").text
        soup = BeautifulSoup(source, 'html.parser')
        for i in soup.findAll("a", {"class": "link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"}):
            if 'ad_business_id' not in i['href']:
                link = "https://www.yelp.com/"+i['href']
                menu_link = link.split('/')
                menu_link[4] = '/menu/'
                menu_link[1] = '//'
                menu_link = ''.join(menu_link)
                menu_page = menu_link 
                # print(link)
                # print(menu_link)
                menu_url = requests.get(menu_link)
                menu_soup = BeautifulSoup(menu_url.content, 'lxml')
                hotel_soup  = BeautifulSoup(menu_url.content, 'lxml')
                restaurantName = hotel_soup.find('h1')
                if restaurantName is None:
                    continue 
                
                restaurantName = restaurantName.text.strip()
                restaurantName = restaurantName.strip('Menu for ')
                # print(restaurantName)
                menu = menu_soup.find("div", {"class": "menu-sections"})
                h2 = menu.find_all("h2")
                for h in h2:
                    section = h.text.strip()
                    items = h.parent.find_next_sibling()
                    h4 = items.find_all("h4")
                    for h44 in h4:
                        itemName=h44.text.strip()
                        price =h44.parent.find_next_sibling()
                        itemPrice = price.find("li", {"class", "menu-item-price-amount"})
                        
                        if itemPrice is None:
                            itemPrice = price.findAll('tr')#container.findAll('tr')
                            l1=[]
                            
                            for p in itemPrice:
                                size = p.find('th').text.strip()
                                pr = p.find('td').text.strip()
                                l1.append(size + ' - ' + pr)
                                itemPrice = ' , '.join(l1)
                        else:
                            itemPrice=itemPrice.text.strip()
                        
                        if len(itemPrice) == 0:
                            itemPrice = ""
                        
                        data.append({"Restaurant":restaurantName, "Category":section, "Item":itemName,"Price":itemPrice})
                        # print({"Hotel":restaurantName, "category":section, "item":itemName,"price":itemPrice})

    # print(data)
    dataset = pd.DataFrame(data,columns=['Restaurant', 'Category', 'Item', 'Price'])
    print(dataset)

restaurant_menu()