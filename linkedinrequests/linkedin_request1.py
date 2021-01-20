from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection
import random
import sys
import traceback


def send_connection_requests():
    
    # User_id = sys.argv[1]
    Email_id = sys.argv[1]
    Password = sys.argv[2]
    keyword = sys.argv[3]
    location = sys.argv[4]
    message = sys.argv[5]
    limit = int(sys.argv[6])
    sleeps = [2,3,4]
    print(Email_id)
    print(Password)
    print(keyword)
    print(location)
    print(message)
    print(limit)

    PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
    # PATH= r"/usr/local/bin/chromedriver"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(PATH,options=chrome_options)

    client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.linkedinContacts

    def otp():
        print("Linkedin sent you an OTP to your email.")
        otp_db = my_db.linkedin_otp
        otp_db.insert({"linkedin_login_url": Email_id, "Status":"OTP sent"})
    # execute "python otp.py <email> <otp>" in another terminal
        flag = True
        while flag:
            data = otp_db.find({"linkedin_login_url": Email_id, "Status":"OTP updated"})
            data = list(data)
            # print(data)
            # print(len(data))
            if len(data) == 1:
                # print(data[0]['OTP'])
                otp = data[0]['OTP']
                # print("otp is: ",otp)
                otp_db.update_many( 
                {"linkedin_login_url":Email_id, "Status":"OTP updated"}, 
                { "$set":{ "Status":"Login complete" }},)
                break
            time.sleep(5)
        # otp = int(input("Please enter the OTP recieved at registered mobile number: "))
        # driver.current_url
        submit_otp = driver.find_element_by_name("pin")
        submit_otp.send_keys(otp)
        submit_otp.send_keys(Keys.RETURN)

    
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

    
    #sign in into linked account
    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_id("username").send_keys(Email_id)
    password = driver.find_element_by_id("password")
    time.sleep(random.choice(sleeps))
    password.send_keys(Password)
    password.send_keys(Keys.RETURN)
    print('Login...')

    
    if 'https://www.linkedin.com/checkpoint' in driver.current_url:
        otp()

    
    my_db.linkedin_otp.drop()

    #Search Mern
    # driver.get("https://www.linkedin.com/feed/")
    chatWindow()
    search = driver.find_element_by_class_name("search-global-typeahead__input ")
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    print("Entered keyword")
    time.sleep(10)

    #clicking on people's tab
    people = driver.find_element_by_xpath("//button[@aria-label='People']")
    people.click()
    time.sleep(random.choice(sleeps))
    #selecting location(India)
    time.sleep(10)
    container = driver.find_element_by_xpath("//button[@aria-label='Locations filter. Clicking this button displays all Locations filter options.']")
    container.click()
    time.sleep(random.choice(sleeps))

    enter_location = driver.find_element_by_xpath("//input[@placeholder='Add a location']")
    # enter_location
    enter_location.send_keys(location)
    time.sleep(5)

    find_location = driver.find_element_by_xpath("//div[@role='listbox']")
    print(find_location)
    select_location = find_location.find_element_by_xpath("//div[@role='option']")
    select_location.click()

    select_location = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
    select_location[1].click()



    # country = driver.find_element_by_xpath("//label[@aria-label='Filter by India']")
    # country.click()
    # time.sleep(random.choice(sleeps))
    # location = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
    # location[1].click()
    time.sleep(random.choice(sleeps))

    url = driver.current_url
    pagination = url
    count = 1
    page = 1
    # limit = 5
    
    while count <= limit:
        chatWindow()

        #For pagination
        pagination = f"{pagination}&page={page}"
        print("Pagination", pagination)
        driver.get(pagination)
        chatWindow()

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
            chatWindow()
            if count <= limit:
                # print("iff")
                try:
#                     print("tryy")
                    #Click on onnect button
                    connect = result.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
                    print("Clicking on Connect")
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
                    add_note.send_keys(message)
                    time.sleep(random.choice(sleeps))
                    
                    #sending note
                    send_req = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                    send_req.click()
                    print("Request Sent")
                    time.sleep(random.choice(sleeps))
                    count +=1 
                    time.sleep(random.choice(sleeps))
                except:
                    print("Connection request already sent...")
#                     traceback.print_exc()
            else:
                break
            driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            if i + 125 < length: #increasing for scroll length
                i += 125
        # print(page)
        page +=1
    print("All requests sent")
send_connection_requests()
