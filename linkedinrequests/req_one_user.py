#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests


# In[223]:


PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
driver = webdriver.Chrome(PATH)


# In[10]:


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')


# In[224]:


driver.get("https://www.linkedin.com/login")


# In[225]:


driver.find_element_by_id("username").send_keys('donnybegins@gmail.com')
password = driver.find_element_by_id("password")
password.send_keys('myaccount')
password.send_keys(Keys.RETURN)


# In[39]:


password


# In[35]:


driver.current_url


# In[206]:


driver.get("https://www.linkedin.com/feed/")


# In[226]:


search = driver.find_element_by_class_name("search-global-typeahead__input ")


# In[227]:


search.send_keys("MERN")


# In[48]:


print(search)


# In[228]:


search.send_keys(Keys.RETURN)


# In[210]:





# In[212]:





# In[181]:


# driver.execute_script("window.history.go(-1)")


# In[75]:


driver.page_source


# In[229]:


# driver.find_element_by_xpath("//div[@id='a']//a[@class='click']"


# In[230]:


people = driver.find_element_by_xpath("//button[@aria-label='People']")
people.click()


# In[231]:


container = driver.find_element_by_xpath("//button[@aria-label='Locations filter. Clicking this button displays all Locations filter options.']")
container


# In[232]:


container.click()


# In[233]:


country = driver.find_element_by_xpath("//label[@aria-label='Filter by India']")
country


# In[234]:


country.click()


# In[220]:


pagination = driver.current_url
pagination


# In[221]:


pagination = f"{pagination}&page=1"
pagination


# In[235]:


li = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
li[1].click()


# In[248]:


result_list = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
len(result_list)


# In[257]:


for enu,result in enumerate(result_list):
    try:
        connect = result.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
        print(connect)
        connect.click()
    except Exception as e:
        print("Connection request already sent")
        print(e)
        
    if enu == 1:
        break


# In[250]:


add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
add_note


# In[251]:


add_note.click()


# In[252]:


add_note = driver.find_element_by_xpath("//textarea[@name='message']")
add_note


# In[253]:


note = 'I have a job opportunity for you'


# In[254]:


add_note.send_keys(note)


# In[255]:


send_req = driver.find_element_by_xpath("//button[@aria-label='Send now']")
send_req


# In[256]:


send_req.click()

