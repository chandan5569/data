# Nooras Fatima 
# https://github.com/nooras

#Importing all libraries
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs4
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import pandas as pd
import re
import requests
import urllib.parse
from time import sleep
import csv
import pymongo
from bson.objectid import ObjectId
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver import ActionChains


#Use Incognito mode when scraping
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--disable-infobars')
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument('--remote-debugging-port=9222')
browser = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)

print("Scrapping Started.")
#Search and getting the page data
# SearchWord = "cancer"
UserID = sys.argv[1] #taking user_id
SearchWord = sys.argv[2] #taking SearchWord
url = "https://www.youtube.com/results?search_query=" + SearchWord
browser.get(url)

x = browser
x.page_source
aTag = x.find_elements_by_xpath('//*[@id="video-title"]') #Finding div of video-title 

#Saving all videoName And VideoHref in aAttribute dict
aAttribute = {}
for a in aTag:
    videoTitle = a.get_attribute("title")
    videoHref = a.get_attribute("href")
    aAttribute[videoTitle] = videoHref
#print(aAttribute)

#Function for getting channel Name and Channel href
def browseChannelUrl(urlBrowse):
    sleep(2)
    browser.get(urlBrowse)
    browser.page_source
    sleep(3)
    channel = browser.find_element_by_xpath('//*[@id="text"]/a')
    channelName = channel.text
    channelHref = channel.get_attribute('href')
    #print(channelName, channelHref)
    return channelName, channelHref

# a, b = browseChannelUrl('https://www.youtube.com/watch?v=SGaQ0WwZ_0I')
# print(a,b)

#Function for Retrieving all link from about page
def aboutRetrieveUrl(urlChannel):
    #link = {}
    sleep(2)
    browser.get(urlChannel)
    browser.page_source
    sleep(2)
    text_list = browser.find_elements_by_xpath("//div[@class='tab-content style-scope paper-tab']")  
    btn = text_list[-1]    # Fetching the text of last element
    # btn.click()
    ActionChains(browser).click(btn).perform()
    # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='tab-content style-scope paper-tab'])[last()]"))).click()
    browser.page_source
    sleep(2)
    data = browser.find_element_by_xpath('//*[@id="links-container"]') 
    aTags = data.find_elements_by_tag_name('a')
    l = [{"Link_Name":a.text, "Link":a.get_attribute('href')} for a in aTags]
    # for a in aTags:
    #     #print(a.text, a.get_attribute('href'))
    #     link[a.text] = a.get_attribute('href')
    return l
    
#aboutRetrieveUrl('https://www.youtube.com/channel/UCkNrj1l4JLvLX7M42fJoLGw')

#Mongodb Connection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
YTData = db.youtubeScriptData #collection

#Going thourgh all dict aAttribuue dict for retrieving all necessary data and saving it in CSV file and into the db
with open('YTScriptData.csv', mode='w') as csv_file:
    fieldnames = ['UserID', 'SearchWord', 'VideoTitle', 'VideoHref', 'ChannelName', 'ChannelHref', 'Links']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for key, value in aAttribute.items(): #dict
        videoTitle = key
        videoHref = value
        sleep(1)
        #print(videoTitle, videoHref)
        if videoHref is None:
            continue
        chanelName, channelHref = browseChannelUrl(videoHref)
        #print(chanelName, channelHref)
        sleep(1)
        aboutLinks = aboutRetrieveUrl(channelHref)
        sleep(1)
        #print(videoTitle, videoHref)
        #print(aboutLinks)
        writer.writerow({'UserID': UserID, 'SearchWord': SearchWord, 'VideoTitle': videoTitle, 'VideoHref': videoHref, 'ChannelName': chanelName, 'ChannelHref':channelHref, 'Links':aboutLinks}) #inserting in csv file
        YTData.insert({'UserID': UserID, 'SearchWord': SearchWord, 'VideoTitle': videoTitle, 'VideoHref': videoHref, 'ChannelName': chanelName, 'ChannelHref':channelHref, 'Links':aboutLinks}, check_keys=False) #Inserting in db
        print("-----One Document Inserted.------")
print("Scrapping Stopped.")

