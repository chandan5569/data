from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection
import sys
import time
import random

def hotel_menu():
#     item = input("Please enter the name of food item: ")
#     place = input("Please enter the location: ")
#     number_of_hotels = int(input("Enter the number of hotels: "))
    User_id = sys.argv[1]
    keyword = sys.argv[2]
    city = sys.argv[3]
    state = sys.argv[4]
    place = city+' '+state
    start = int(sys.argv[5])
    if start == 1:
        start = 0
    else:
        start = 10*start-10
    end = int(sys.argv[6])
    end = 10*end-10
    print(User_id)
    print(place)
    print("Scraping started")
    # print(place)

    client = pymongo.MongoClient('mongodb+srv://bilalm:'+urllib.parse.quote_plus('Codemarket.123')+'@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.hotel_menu
    
    
    sleeps = [1,2,3,4]
    for i in range (start, end+10, 10):
#         if end > start:
#             break
        source = requests.get(f"https://www.yelp.com/search?find_desc={keyword}&find_loc={place}&ns=1&start={i}").text
        # print(f"https://www.yelp.com/search?find_desc={keyword}&find_loc={place}&ns=1&start={start}")
        soup = BeautifulSoup(source, 'html.parser')
        time.sleep(random.choice(sleeps))
        

        for i in soup.findAll("a", {"class": "link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"}):         

            restaurant_data = []
            
            if 'ad_business_id' not in i['href']:
                link = "https://www.yelp.com/"+i['href']
                menu_link = link.split('/')
                menu_link[4] = '/menu/'
                menu_link[1] = '//'
                menu_link = ''.join(menu_link)
                menu_page = menu_link 
                # print(link)
                # print("Hotel menu- " +menu_page)
                menu_url = requests.get(menu_link)
                menu_soup = BeautifulSoup(menu_url.content, 'html.parser')
                time.sleep(random.choice(sleeps))
                hotel_soup  = BeautifulSoup(menu_url.content, 'html.parser')
                hotel_name = hotel_soup.find('h1')
                # print(hotel_name)
                # print(hotel_name)
                # break
                if hotel_name is None:
                    continue 
                # if "Menu" not in hotel_name:
                #     continue
                
                hotel_name = hotel_name.text.strip()
                hotel_name = hotel_name.split(' ')[2:]
                hotel_name = ' '.join(hotel_name)
                menu = menu_soup.find("div", {"class": "menu-sections"})
                if menu == None:
                    continue
                h2 = menu.find_all("h2")
                
                for h in h2:
                    section_data = []
                    section = h.text.strip()
                    items = h.parent.find_next_sibling()
                    h4 = items.find_all("h4")
                    
                    for h44 in h4:
                        data = []
                        name_result=h44.text.strip()
                        price =h44.parent.find_next_sibling()
                        price_result = price.find("li", {"class", "menu-item-price-amount"})
                        
                        if price_result is None:
                            price_result = price.findAll('tr')
                            quantity=[]
                            for p in price_result:
                                size = p.find('th').text.strip()
                                pr = p.find('td').text.strip()
                                quantity.append({"Quantity": size, "Price": pr})
                                price_result = quantity
                        else:
                            price_result=price_result.text.strip()
                        
                        if len(price_result) == 0:
                            price_result = ""
                        section_data.append({"Item":name_result,"Price":price_result})
                    
                   
                    restaurant_data.append({"Category":section, "Items": section_data}) 
                    time.sleep(random.choice(sleeps))
                db.insert({"User_Id": User_id, "Keyword": keyword, "City": city, "State":state, "Restaurant_Name": hotel_name,"Restaurant_Menu": restaurant_data})
                
                
                
           
    print("Scraping stopped")
    dataset = pd.DataFrame(restaurant_data,columns=['Menu'])
    dataset.to_csv(keyword+'.csv')

hotel_menu()