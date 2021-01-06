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

#Use Incognito mode when scraping
chrome_options = Options()
chrome_options.add_argument(" — incognito")
browser = webdriver.Chrome(options=chrome_options)

#Serach and getting the page data
SearchWord = "cancer"
url = "https://www.youtube.com/results?search_query=" + SearchWord
browser.get(url)

x = browser
browser.page_source
aTag = x.find_elements_by_xpath('//*[@id="video-title"]') #Finding div of video-title 

#Function for getting channel Name and Channel href
def browseChannelUrl(urlBrowse):
    browser.get(urlBrowse)
    browser.page_source
    channel = browser.find_element_by_xpath('//*[@id="text"]/a')
    channelName = channel.text
    channelHref = channel.get_attribute('href')
    #print(channelName, channelHref)
    return channelName, channelHref

# a, b = browseChannelUrl('https://www.youtube.com/watch?v=SGaQ0WwZ_0I')
# print(a,b)

#Function for Retrieving all link from about page
def aboutRetrieveUrl(urlChannel):
    link = {}
    browser.get(urlChannel)
    browser.page_source
    btn = browser.find_element_by_xpath('//*[@id="tabsContent"]/paper-tab[6]/div')
    btn.click()
    browser.page_source
    data = browser.find_element_by_xpath('//*[@id="links-container"]') 
    aTag = data.find_elements_by_tag_name('a')
    for a in aTag:
        #print(a.text, a.get_attribute('href'))
        link[a.text] = a.get_attribute('href')
    return link
    
#aboutRetrieveUrl('https://www.youtube.com/channel/UCkNrj1l4JLvLX7M42fJoLGw')

#Going thourgh all div of video-title and retrieving all necessary data
for a in aTag:
    print(a.get_attribute("title"))
    print(a.get_attribute("href"))
    videoTitle = a.get_attribute("title")
    videoHref = a.get_attribute("href")
    sleep(1)
    chanelName, channelHref = browseChannelUrl(videoHref) #Call
    sleep(1)
    aboutLink = aboutRetrieveUrl(channelHref) #Call
    sleep(1)
    #print(videoTitle, videoHref)
    print(chanelName, channelHref)
    print(aboutLink)
    print("---------------")

# Getting selenium.common.exceptions.StaleElementReferenceException this exception !! Only 1 loop works !! Csv !! Pending!!