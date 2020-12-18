import requests 
from bs4 import BeautifulSoup
import pymongo
from mongoengine import *
from mongoengine.context_managers import switch_collection
import urllib.parse
import argparse
import datetime
import pandas as pd

class Website(EmbeddedDocument):
    restaurant_name = StringField(max_length=250, required=True)
    city = StringField()
    keyword = StringField(max_length=250)
    menu_data = []

class Menu_scraper(Document):
    userid = StringField(max_length=120, required=True)
    name = StringField(max_length=120, required=True)
    status = StringField(max_length=120)
    city = StringField(max_length=250)
    keywords = ListField(StringField(max_length=250))
    created_timestamp = DateTimeField()
    last_updated = DateTimeField()
    collection_of_menu_scraped = EmbeddedDocumentListField(Website)

class Scraper:
    def __init__(self,userid,name,keyword,city):
        self.userid = userid
        self.name = name
        self.keyword = keyword
        self.collections = "Menu"
        self.city = city
        self.all_websites = []
        self.final_result = set()
        try:
            self.get_scraped_data()
        except:
            print(f"{self.userid} has no data available for {self.name}")

    def create_db(self, collection, query):
        status = 'Scraping Started'
        document = collection.find_one(query)
        
        if document:
            return document
        else:
            document = {'userid':self.userid,
                        'name':self.name,
                        'keywords':[self.keyword],
                        'city':[self.city],
                        'status': status,                    
                    }
            collection.insert_one(document)
    
    def get_scraped_data(self):
        client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
        query={'userid': self.userid,'name': self.name}
        db = client["codemarket_shiraz"]
        collection = db[self.collections]
        document = self.create_db(collection, query)
        if document:
            data_menu = document["collection_of_menu_scraped"]
            # print(data_menu)
            dataframe = pd.DataFrame(data_menu)
            # print(dataframe)
            col = dataframe.restaurant_name.to_list()
            self.all_websites = col
            

    def get_url(self, start=0):
        # https://www.yelp.com/search?find_desc=Indian+Food&find_loc=Redondo+Beach%2C+CA&ns=1&start={start}
        desc = self.keyword
        loc = self.city
        url = f'https://www.yelp.com/search?find_desc={desc}&find_loc&={loc}&ns=1&start={start}'
        return url

    def scrape(self, Menu_scraper):
        print('Begin Scraping')
        connect(db = 'codemarket_shiraz', host = 'mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
        with switch_collection(Menu_scraper, self.collections) as Menu_scraper:
            data = []
            for start in range (0, 10, 10):
                Menu_scraper.objects(userid = self.userid, name = self.name).update(push__keywords = self.keyword)
                url = self.get_url(start)
                source = requests.get(url).text
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
                        status = 'Scraping Restaurant Menu'
                        Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = status)
                        menu_url = requests.get(menu_link)
                        menu_soup = BeautifulSoup(menu_url.content, 'lxml')
                        hotel_soup  = BeautifulSoup(menu_url.content, 'lxml')
                        restaurantName = hotel_soup.find('h1')
                        if restaurantName is None:
                            continue 
                        restaurantName = restaurantName.text.strip()
                        restaurantName = restaurantName.strip('Menu for ')
                        # print(restaurantName)
                        if restaurantName in self.all_websites:
                            print("Restaurant data already available")
                        else:
                            self.all_websites.append(restaurantName)
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
                                    website_object = Website()
                                    website_object.restaurant_name = restaurantName
                                    website_object.keyword = self.keyword
                                    website_object.city = self.city
                                    website_object.menu_data = data

                                    try:
                                        Menu_scraper.objects(userid = self.userid, name = self.name).update(push__collection_of_menu_scraped = website_object)
                                        Menu_scraper.objects(userid = self.userid, name = self.name).update(set__last_updated = datetime.datetime.now())
                                    except:
                                        print("Not Unique data")
            # print(data)
            dataset = pd.DataFrame(data,columns=['Restaurant', 'Category', 'Item', 'Price'])
            # print(dataset)

        Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = "Scraping Completed")
                   
        print('End Scraping')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('userid',type=str,nargs='?',default='shiraz',help='Enter userid')
    parser.add_argument('name',type=str,nargs='?',default='menu_scraper',help='Enter name')
    parser.add_argument('keyword',type=str,nargs='?',default=urllib.parse.quote_plus('Indian Food'),help='Enter keyword')
    parser.add_argument('city',type=str,nargs='?',default=urllib.parse.quote_plus('Redondo Beach, CA'),help='Enter city')
    args = parser.parse_args()

    userid = args.userid
    name = args.name
    keyword = args.keyword
    city = args.city
    print(userid, name, keyword, city)

    scraper_obj = Scraper(userid,name,keyword,city)
    scraper_obj.scrape(Menu_scraper)
