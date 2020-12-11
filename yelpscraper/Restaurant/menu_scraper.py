from requests import get
from bs4 import BeautifulSoup
import re
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pymongo
from mongoengine import *
from mongoengine.context_managers import switch_collection
import urllib.parse
import argparse
import datetime
from sys import stdout
import pandas as pd

class Website(EmbeddedDocument):
    business_name = StringField(max_length=250, required=True)
    website_link = StringField(max_length=250, required=True)


class Menu_scraper(Document):
    userid = StringField(max_length=120, required=True)
    name = StringField(max_length=120, required=True)
    status = StringField(max_length=120)
    city = StringField(max_length=250)
    keywords = ListField(StringField(max_length=250))
    created_timestamp = DateTimeField()
    last_updated = DateTimeField()
    # collection_of_menu_scraped = EmbeddedDocumentListField(Website)

class Scraper:
    def __init__(self,userid,name,keyword,city):
        self.userid = userid
        self.name = name
        self.keyword = keyword
        self.collections = "Yelp"
        self.city = city
        # self.all_websites = []
        # self.final_result = set()
        # try:
            # self.get_scraped_data()
        # except:
            # print(f"{self.userid} has no data available for {self.name}")

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
            # print(data_menu)
            dataframe = pd.DataFrame(data_menu)
            # print(dataframe)
            col1 = dataframe.business_name.to_list()
            col2 = dataframe.website_link.to_list()
            # print(col1, col2,)
            self.all_websites = col1

    def get_url(self):
        # https://www.yelp.com/search?find_desc=Indian+Food&find_loc=Redondo+Beach%2C+CA
        desc = self.keyword
        loc = self.city
        url = f'https://www.yelp.com/search?find_desc={desc}&find_loc&={loc}'
        return url

    def scrape(self, Menu_scraper):
        self.flag = 0
        print('Begin Scraping')
        connect(db = 'codemarket_shiraz', host = 'mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
        while self.flag < 10:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument('--disable-dev-shm-usage')
            # driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
            driver = webdriver.Chrome('/home/dhruv034/Desktop/codemarket/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
            #driver = webdriver.Chrome('E:/Codes/chromedriver.exe')#,chrome_options=chrome_options)
            try:
                with switch_collection(Menu_scraper, self.collections) as Menu_scraper:
                    if self.flag == 0:
                        Menu_scraper.objects(userid = self.userid, name = self.name).update(push__keywords = self.keyword)
                        # Explicit wait for the site to load for slow internet connection
                        wait = WebDriverWait(driver, 10)
                        # Get the url using keyword and city
                        url = self.get_url()
                        # print(url)
                        driver.get(url)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        # Find the business(Restaurant) list from the searched url 
                        rest_list = soup.find('ul',class_="undefined list__09f24__17TsU")
                        lilist = rest_list.findChildren(['li'])
                        for li in lilist:
                            link = li.find('a',class_="link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95")
                            if link == None:
                                continue
                            driver.get("https://yelp.com/" + link['href'])
                            rest_page = driver.page_source
                            rest_soup = BeautifulSoup(rest_page, 'html.parser')
                            rest_name = rest_soup.find('h1',class_ = "lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy").text
                            print(rest_name)

                            # Click on the Takeout tab
                            tab = wait.until(EC.element_to_be_clickable((
                                By.XPATH, '//div[@class="lemon--div__373c0__1mboc tab__373c0__24QGW tabNavItem__373c0__3X-YR tab--section__373c0__3V0A9 tab--no-outline__373c0__3adQG"]'
                            )))
                            tab.click()
                            # Click on the Start Order button
                            order = wait.until(EC.element_to_be_clickable((
                                By.XPATH, '//button[@class="button__373c0__3lYgT primary__373c0__2ZWOb full__373c0__1AgIz"]'
                            )))
                            order.click()
                            status = 'Scraping website'
                            Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = status)
                            time.sleep(3)
                            menu_link = driver.current_url
                            menu_page = driver.page_source
                            menu_soup = BeautifulSoup(menu_page, 'html.parser')
                            print("Parsed cart page")
                    
                    Menu_scraper.objects(userid = self.userid, name = self.name).update(set__status = "Scraping Completed")
                    break

            except AttributeError:
                self.flag += 1
                print(f"trial:{self.flag}")
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
