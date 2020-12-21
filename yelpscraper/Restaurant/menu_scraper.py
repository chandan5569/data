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
    restaurantName = StringField(max_length=250, required=True)
    city = StringField()
    keyword = StringField(max_length=250)
    menuData = DictField()

class Menu_scraper(Document):
    userid = StringField(max_length=120, required=True)
    name = StringField(max_length=120, required=True)
    status = StringField(max_length=120)
    cities = ListField(StringField(max_length=250))
    keywords = ListField(StringField(max_length=250))
    created_timestamp = DateTimeField()
    lastUpdated = DateTimeField()
    collectionOfMenuScraped = EmbeddedDocumentListField(Website)

class Scraper:
    def __init__(self,userid,name,keyword,city):
        self.userid = userid
        self.name = name
        self.keyword = keyword
        self.collections = "MenuData"
        self.city = city
        self.all_websites = []
        self.menuData = {}
        self.final_result = set()
        try:
            self.get_scraped_data()
        except:
            print(f"{self.userid} has no data available for {self.name}")

    # Creating a document in mongodb
    def create_db(self, collection, query):
        status = 'Scraping Started'
        document = collection.find_one(query)
        
        if document:
            return document
        else:
            document = {'userid':self.userid,
                        'name':self.name,
                        'keywords':[self.keyword],
                        'cities':[self.city],
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
            data_menu = document["collectionOfMenuScraped"]
            # print(data_menu)
            dataframe = pd.DataFrame(data_menu)
            # print(dataframe)
            col = dataframe.restaurantName.to_list()
            self.all_websites = col
            
    # Generate a url for given search
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
            menu_dict={}
            data = []
            for start in range (0, 20, 10):
                Menu_scraper.objects(userid = self.userid, name = self.name).update(push__keywords = self.keyword)
                Menu_scraper.objects(userid = self.userid, name  = self.name).update(push__cities =self.city)
                url = self.get_url(start)
                source = requests.get(url).text
                soup = BeautifulSoup(source, 'html.parser')
                for i in soup.findAll("a", {"class": "link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95"}):
                    if 'ad_business_id' not in i['href']:
                        link = "https://www.yelp.com/"+i['href']
                        menu_link = link.split('/')
                        menu_link = link.replace("biz", "menu")
                        # print(link)
                        # print(menu_link)
                        status = 'Scraping Restaurant Menu'
                        Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = status)
                        
                        menu_url = requests.get(menu_link).text
                        menu_soup = BeautifulSoup(menu_url, 'html.parser')

                        # Find restaurant name
                        rest_name = menu_soup.find('h1')
                        if rest_name == None:
                            continue
                        rest_name = rest_name.text.strip()
                        rest_name = rest_name.strip("Menu for ")
                        # print(rest_name)

                        if rest_name in self.all_websites:
                            print(rest_name +" data already available. ")
                        else: 
                            self.all_websites.append(rest_name)

                            # Find Category list like Appetizers, salads etc 
                            category_list = []
                            for j in menu_soup.find_all('div',{"class":"section-header"}):
                                category = j.find('h2')
                                c = category.text.strip()
                                category_list.append(c)
                            # print(category_list)

                            # Scrap menu-item and menu-item-price for each category
                            menu = {}
                            menu_list = []
                            count = 0
                            for j in menu_soup.find_all('div', {"class": "u-space-b3"}):
                                menu_item = []
                                menu_item_price = []
                                for i in j.find_all('div', {"class": "menu-item"}):
                                    menu_item_name = i.find('h4')
                                    menu_item_name = menu_item_name.text.strip()
                                    menu_item.append(menu_item_name)
                                    item_price = i.find('div',{"class": "menu-item-prices"})
                                    item_price = item_price.text.strip()
                                    menu_item_price.append(item_price)

                                data = {'itemName': menu_item, 'itemPrice':menu_item_price}
                                df = pd.DataFrame(data=data)
                                # menu[category_list[count]] = df.to_dict("records")
                                menu_list.append( { 'category':category_list[count], 'categoryItems': df.to_dict("records")  })
                                count += 1
                                if count == len(category_list):
                                    break
                                menu = {'restaurantName': rest_name, 'menuList': menu_list}

                            website_object = Website()
                            website_object.restaurantName = rest_name
                            website_object.menuData = menu
                            website_object.keyword = self.keyword
                            website_object.city = self.city

                            try:
                                Menu_scraper.objects(userid = self.userid, name = self.name).update(push__collectionOfMenuScraped = website_object)
                                Menu_scraper.objects(userid = self.userid, name = self.name).update(set__lastUpdated = datetime.datetime.now())
                            except:
                                print("Not Unique data")            

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
