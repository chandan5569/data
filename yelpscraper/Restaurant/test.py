from requests import get
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
import pandas as pd
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
driver = webdriver.Chrome('/home/dhruv034/Desktop/codemarket/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
#driver = webdriver.Chrome('E:/Codes/chromedriver.exe')#,chrome_options=chrome_options)

url = "https://www.yelp.com/search?find_desc=Indian+food&find_loc=Redondo+Beach%2C+CA"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text('Start Order')).click()

rest_list = soup.find('ul',class_="undefined list__09f24__17TsU")
lilist = rest_list.findChildren(['li'])
# Explicit wait for the site to load for slow internet connection
wait = WebDriverWait(driver, 10)
# print(lilist)
for li in lilist[5:23]:
    links = li.findChildren(['a'])
    # print(links.text)
       
    if links == []:
        continue
    print(links)