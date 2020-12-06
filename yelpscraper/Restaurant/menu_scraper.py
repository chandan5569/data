from requests import get
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pymongo
from mongoengine import *
from mongoengine.context_managers import switch_collection
import urllib.parse
import argparse
import datetime
from sys import stdout
import pandas as pd

class Website(EmbeddedDocument):
    restaurant_name = StringField(max_length=250, required= True)
    restaurant_link = StringField(max_length=250, required= True)
    menu = ListField()

class Menu_scraper(Document):
    userid = StringField(max_length=120, required=True)
    name = StringField(max_length=120, required=True)
    status = StringField(max_length=120)
    city = StringField(max_length=250)
    keywords = ListField(StringField(max_length=250))
    menu_counter = IntField()
    limit = StringField()
    created_timestamp = DateTimeField()
    last_updated = DateTimeField()
    collection_of_menu_scraped = EmbeddedDocumentListField(Website)

class Scraper:
    def __init__(self,userid,name,keyword,city,start_limit,end_limit):
        self.userid = userid
        self.name = name
        self.keyword = keyword
        self.collections = "Yelp"
        self.city = city
        self.start_limit = start_limit
        self.end_limit = end_limit
        self.counter = 0
        self.AllInternalLinks = set()
        self.all_websites = []
        self.final_result = set()
        self.menu_counter = 0 
        try:
            self.getScrapedData()
        except:
            print(f"{self.userid} has no data available for {self.name}.")

    def getInternalLinks(self,bsobj, includeurl):
        internalLinks = []
        for links in bsobj.findAll("a", {"href": re.compile("^(/|.*" + includeurl + ")")}):
            if links.attrs['href'] is not None:
                if links.attrs["href"] not in internalLinks:
                    internalLinks.append(links.attrs['href'])                   
        
        for link in internalLinks:
             truncURL = link.replace("http://", "").replace("https://", "").replace(includeurl, "")
             sep = "/"
             spliturl = truncURL.split(sep,2)
             if len(spliturl)>=2:
                 truncURL = spliturl[1] 
                 removeParameterURL = spliturl[1].split("?", 1)
                 if len(removeParameterURL) >=1:
                     truncURL = removeParameterURL[0]
                 else:
                     truncURL = ""
             if truncURL not in self.AllInternalLinks:
                 if link != "http://"+includeurl and link != "https://"+includeurl and link != '/' and link != "http://"+includeurl+'/' and link != "https://"+includeurl+'/':
                    self.AllInternalLinks.add(truncURL)
                    try:
                        websitepage = get("http://"+includeurl+"/" + truncURL)
                    except:
                        continue
                    

                    websitepage_soup = BeautifulSoup(websitepage.text, 'html.parser')
                    self.getInternalLinks(websitepage_soup,includeurl)
        return (internalLinks)

    def create_db(self, collection, query):
        status = 'Scraping Started'
        document = collection.find_one(query)
        
        if document:
            return document
        else:
            document = {'userid':self.userid,
                        'name':self.name,
                        'keywords':[self.keyword],
                        'city':self.city,
                        'limit':f"{self.start_limit} - {self.end_limit}",
                        'status': status
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
            dataframe = pd.DataFrame(data_menu)
            col = dataframe.restaurant_name.to_list()
            self.all_websites = col

    def get_url(self, start=0):
        # https://www.yelp.com/search?find_desc=<Restaurant_name>&find_loc=San+Francisco%2C+CA&ns=
        desc = self.keyword # Type of food
        loc = self.city
        url = f'https://www.yelp.com/search?find_desc={desc}&find_loc={loc}'
        return url

    def splitaddress(self,address):
        return (address.replace("http://", "").replace("https://", "").split("/"))

    def scrape(self, Menu_scraper):
        self.flag = 0
        self.no_menu = True
        print("Begin Scraping")
        connect(db = 'codemarket_shiraz', host = 'mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
        while self.no_menu and self.flag < 10:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument('--disable-dev-shm-usage')
            # driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
            driver = webdriver.Chrome('/home/dhruv034/Desktop/codemarket/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
            # driver = webdriver.Chrome('E:/Codes/chromedriver.exe')#,chrome_options=chrome_options)
            try:
                with switch_collection(Menu_scraper, self.collections) as Menu_scraper:
                    if self.flag == 0:
                        Menu_scraper.objects(userid = self.userid, name = self.name).update(push__keywords = self.keyword)
                        Menu_scraper.objects(userid = self.userid, name = self.name).update(set__limit = f"{self.start_limit} - {self.end_limit}")
                        for start in range((self.start_limit -1) * 10, self.end_limit * 10 , 10):
                            url = self.get_url(start)
                            # print(url)
                            driver.get(url)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            restaurant_list = soup.find('ul',class_=" undefined list__09f24__17TsU")
                            # print(restaurant_list)

                            lilist = restaurant_list.findChildren(['li'])
                            for li in lilist:
                                status = "Scraping website"
                                self.menu_counter = 0 
                                Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = status)
                                link = li.find('a',class_=" link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95")

                                if link == None:
                                    continue

                                driver.get("https://www.yelp.com/" + link['href'])
                                time.sleep(3)
                                profile = driver.page_source
                                profile_soup = BeautifulSoup(profile, 'html.parser')
                                websitelink = None
                                restaurant_name = profile_soup.find('h1',class_=" lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy").txt
                                print(restaurant_name)

                                if profile_soup.find("p", string="Restaurant website") != None:
                                    if profile_soup.find("p", string="Restaurant website").findNext('p') != None:
                                        if profile_soup.find("p", string="Restaurant website").findNext('p').find('a') != None:
                                            websitelink = profile_soup.find("p", string="Restaurant website").findNext('p').find('a')

                                if websitelink == None:
                                    print("Link Not Found")
                                    print("https://www.yelp.com/" + link['href'])
                                    continue

                                if restaurant_name == None:
                                    print("No Restaurant")
                                    restaurant_name = websitelink
                                print(restaurant_name)

                                if restaurant_name in self.all_websites:
                                    print("Restaurant data already available")
                                else:
                                    self.all_websites.append(restaurant_name)

                                try:
                                    driver.get("http://"+websitelink.text)
                                except:
                                    print("An exception occurred")
                                    continue
                                time.sleep(5)
                                site_url = "http://"+websitelink.text
                                print(site_url)
                                websitepage = driver.page_source
                                websiteSoup = BeautifulSoup(websitepage, 'html.parser')

                                self.getInternalLinks(websiteSoup, self.splitaddress(websitelink.text)[0])
                                self.AllInternalLinks.clear()

                                website_object = Website()
                                website_object.restaurant_name = restaurant_name
                                website_object.restaurant_link = site_url
                                # website_object.menu = Menu;

                                try: 
                                    Menu_scraper.objects(userid = self.userid, name = self.name).update(push__collection_of_menu_scraped = website_object)
                                    Menu_scraper.objects(userid = self.userid, name = self.name).update(inc__menu_counter = self.menu_counter)
                                    Menu_scraper.objects(userid = self.userid, name = self.name).update(set__last_updated = datetime.datetime.now())
                                except:
                                    print("Not unique data")
                    
                    Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status ="Scraping Completed")
                    break
            except AttributeError:
                self.flag += 1  
                print(f"trial:{self.flag}")
        print('End Scraping')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('userid',type=str,nargs='?',default='shiraz',help='Enter userid')
    parser.add_argument('name',type=str,nargs='?',default='yelp_scraper',help='Enter name')
    parser.add_argument('keyword',type=str,nargs='?',default=urllib.parse.quote_plus('Indian Food'),help='Enter keyword')
    parser.add_argument('city',type=str,nargs='?',default=urllib.parse.quote_plus('Manhattan'),help='Enter city')
    parser.add_argument('start_limit',type=int,nargs='?',default=1, help='Enter limit')
    parser.add_argument('end_limit',type=int,nargs='?',default=5, help='Enter limit')
    args = parser.parse_args()

    userid = args.userid
    name = args.name
    keyword = args.keyword
    city = args.city
    start_limit = args.start_limit
    end_limit = args.end_limit
    print(userid, name, keyword, city, start_limit, end_limit)

    scraper_obj = Scraper(userid,name,keyword,city,start_limit, end_limit)
    scraper_obj.scrape(Menu_scraper)                                