#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import sys
import time
import random


# In[103]:


PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
driver = webdriver.Chrome(PATH)
chrome_options = Options()
sleeps = [2,3,4]

#sign in into linked account
driver.get("https://www.linkedin.com/login")
driver.find_element_by_id("username").send_keys('donnybegins@gmail.com')
password = driver.find_element_by_id("password")
time.sleep(random.choice(sleeps))
password.send_keys('myaccount')
password.send_keys(Keys.RETURN)




# In[104]:


driver.get("https://www.linkedin.com/feed/")
search = driver.find_element_by_class_name("search-global-typeahead__input ")
search.send_keys("MERN")
search.send_keys(Keys.RETURN)
time.sleep(10)
#clicking on people's tab
people = driver.find_element_by_xpath("//button[@aria-label='People']")
people.click()

length = driver.execute_script("return document.documentElement.scrollHeight")
for i in range(100, length, 100):
    driver.execute_script("window.scrollTo(0, " + str(i) + ")")
    time.sleep(2)

#selecting location(India)
container = driver.find_element_by_xpath("//button[@aria-label='Locations filter. Clicking this button displays all Locations filter options.']")
container.click()
country = driver.find_element_by_xpath("//label[@aria-label='Filter by India']")
country.click()

location = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
location[1].click()


# In[109]:


def send_connection_requests():
    
#     User_id = sys.argv[1]
#     Email_id = sys.argv[2]
#     Password = sys.argv[3]
#     keyword = sys.argv[4]
#     limit = sys.argv[5]
    limit = 15
    sleeps = [2,3,4]
    

    pagination = driver.current_url
    count = 1
    page = 1
    while count <= limit:
        
        
        pagination = f"{pagination}&page={page}"
        print(pagination)
        
        #list for search result
        driver.get(pagination)
        length = driver.execute_script("return document.documentElement.scrollHeight")
        for i in range(100, length, 100):
            driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            time.sleep(2)
        result_list = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
#         print(result_list)
        time.sleep(5)
        for enu,result in enumerate(result_list):

            print(result)
#             continue
            time.sleep(5)
            if count <= limit:
                print("trying")
                try:
                    connect = result.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
                    print(connect)
                    time.sleep(5)
                    
                    connect.click()
                    time.sleep(random.choice(sleeps))
                    print("sending req")
                               
                    add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                    add_note.click()
                    time.sleep(random.choice(sleeps))
                               
                    add_note = driver.find_element_by_xpath("//textarea[@name='message']")
                    add_note.send_keys('I have a job opportunity for you.')
                               
                    time.sleep(random.choice(sleeps))
                    send_req = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                    send_req.click()
#                     break
                    time.sleep(random.choice(sleeps))
                    count +=1 
                    
                    time.sleep(random.choice(sleeps))
                except:
                    print("Connection request already sent")
                    traceback.print_exc()
                    
        
        page +=1
        print(page)
        break

    


# In[110]:


send_connection_requests()


# In[ ]:





# In[ ]:




