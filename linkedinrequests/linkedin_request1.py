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
import traceback

# In[103]:

#For closing chat window
def chatWindow():
    try:
        chatOpen = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/div")
        if chatOpen:
            chatClose = driver.find_element_by_xpath("(//*[@id='msg-overlay']/div[1]/header/section[1])")
            chatClose.click()
            print("Chatbox Closed...")
            return True
    except:
        print("Chatbox is already closed")
        return True

# PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
chrome_options = Options()
#chrome_options.add_argument("--window-size=1920,1200");
driver = webdriver.Chrome(options=chrome_options)
sleeps = [2,3,4]

#sign in into linked account
driver.get("https://www.linkedin.com/login")
driver.find_element_by_id("username").send_keys('donnybegins@gmail.com')
password = driver.find_element_by_id("password")
time.sleep(random.choice(sleeps))
password.send_keys('myaccount')
password.send_keys(Keys.RETURN)
print('Login...')

# In[104]:

#Search Mern
driver.get("https://www.linkedin.com/feed/")
chatWindow()
search = driver.find_element_by_class_name("search-global-typeahead__input ")
search.send_keys("MERN")
search.send_keys(Keys.RETURN)
time.sleep(10)

#clicking on people's tab
people = driver.find_element_by_xpath("//button[@aria-label='People']")
people.click()

#selecting location(India)
time.sleep(10)
container = driver.find_element_by_xpath("//button[@aria-label='Locations filter. Clicking this button displays all Locations filter options.']")
container.click()
country = driver.find_element_by_xpath("//label[@aria-label='Filter by India']")
country.click()
location = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
location[1].click()


# In[109]:

url = driver.current_url
def send_connection_requests():
    
#     User_id = sys.argv[1]
#     Email_id = sys.argv[2]
#     Password = sys.argv[3]
#     keyword = sys.argv[4]
#     limit = sys.argv[5]
    limit = 15
    sleeps = [2,3,4]
    pagination = url
    count = 1
    page = 1
    while count <= limit:
        chatWindow()

        #For pagination
        pagination = f"{pagination}&page={page}"
        print("Pagination", pagination)
        driver.get(pagination)

        #Getting length of scroll
        length = driver.execute_script("return document.documentElement.scrollHeight")
        # print("length", length)

        #list for search result
        result_list = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
        # print(result_list)
        time.sleep(5)
        i = 125 #Initialization for scroll
        for enu,result in enumerate(result_list):
            #driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            #print(result)
            # continue
            time.sleep(5)
            if count <= limit:
                # print("iff")
                try:
                    print("tryy")
                    #Click on onnect button
                    connect = result.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
                    print("Connect", connect)
                    time.sleep(5)

                    connect.click()
                    #ActionChains(driver).click(connect).perform()
                    time.sleep(random.choice(sleeps))
                    print("Sending request...")

                    #adding Note
                    add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                    add_note.click()
                    time.sleep(random.choice(sleeps))
                    add_note = driver.find_element_by_xpath("//textarea[@name='message']")
                    add_note.send_keys('Hello, Hope you are doing well. I would like to add you to my professional network on LinkedIn. Thanks')
                    time.sleep(random.choice(sleeps))
                    
                    #sending note
                    send_req = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                    send_req.click()
                    time.sleep(random.choice(sleeps))
                    count +=1 
                    time.sleep(random.choice(sleeps))
                except:
                    print("Connection request already sent...")
                    traceback.print_exc()
            driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            if i + 125 < length: #increasing for scroll length
                i += 125
        page +=1
        print(page)

# In[110]:


send_connection_requests()


# In[ ]:





# In[ ]:




