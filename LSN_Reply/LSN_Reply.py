from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import sys
import time
import random
import traceback
from time import sleep
import urllib.parse
import pymongo
import ast

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument("--window-size=1920,1200");
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

#Taking Input
EmailId = sys.argv[1]

Password = sys.argv[2]

ReplyMsg = sys.argv[3]

Limit = int(sys.argv[4])

#DB connection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
otp_collection = db.OTP_linkedin #collection

#OTP 
def otp():
    print("Linkedin sent you an OTP to your email.")
    otp_collection.insert({"linkedin_login_url": EmailId, "Status":"OTP sent"})
    while True:
        data = otp_collection.find({"linkedin_login_url": EmailId, "Status":"OTP updated"})
        data = list(data)
        # print(data)
        # print(len(data))
        if len(data) == 1:
            # print(data[0]['OTP'])
            otpget = data[0]['OTP']
            # print("otp is: ",otp)
            otp_collection.update_many( 
            {"linkedin_login_url":EmailId, "Status":"OTP updated"}, 
            { "$set":{ "Status":"Login complete" }},)
            print("Found OTP")
            break
        print("Waiting for correct OTP...")
        sleep(15)
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otpget)
    submit_otp.send_keys(Keys.RETURN)

    if driver.current_url == 'https://www.linkedin.com/checkpoint/challenge/verify':
        print("Dropping collection")
        sleep(2)
        otp_collection.drop()
        print("Incorrect OTP. Enter correct otp.")
        print(driver.current_url)
        #otp_collection.drop()
        otp()

    if 'https://www.linkedin.com/feed' in driver.current_url:
        print("Dropping collection")
        sleep(2)
        otp_collection.drop()
        print("Login from Otp...")
        return True
    else:
        print("Session Expired try login again...")
        LSN_Reply()
    print("No return...")


def LSN_Reply():
    
    #Sign in into linked account
    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_id("username").send_keys(EmailId)
    password = driver.find_element_by_id("password")
    sleep(2)
    password.send_keys(Password)
    password.send_keys(Keys.RETURN)

    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit' or "login-submit" in driver.current_url:
        print("Incorrect login details")

    if 'https://www.linkedin.com/checkpoint/lg/login?errorKey=challenge_global_internal_error' in driver.current_url:
        print("Sorry something went wrong. Please try again later")

    print("Current Url : " + driver.current_url)
    if "https://www.linkedin.com/checkpoint" in driver.current_url:
        print("OTP...")
        value = otp()
        if value == True:
            print("Redirected to Feed Page after login.")
        else:
            print("Something went wrong!!")

    if 'https://www.linkedin.com/feed' in driver.current_url:
        print("Login...")
    else:
        print("Something is wrong!! Try again!! Network Problem!!")
        print(driver.current_url)

    #Finding 
    try: 
        #Redirected to LSN Inbox Page
        print("Redirected to Linkedin Sales Navigator Inbox Page.")
        driver.get("https://www.linkedin.com/sales/inbox")
        
        sleep(20) #Longer wait for page load

        #Connection list 
        ul = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
        count = 1

        #Going through each connection
        for x in ul.find_elements_by_xpath("./li"):

            #Selection 1 connection 
            sleep(2)
            a = x.find_element_by_tag_name('a')
            # print(a)
            a.click()
            sleep(2)

            #Chat Inbox
            inbox = driver.find_element_by_xpath("//*[@class='flex flex-column flex-grow-1 flex-shrink-zero justify-flex-end ember-view']/ul")
            print(len(inbox.find_elements_by_xpath("./li")))

            #Going through each chat message
            for i in inbox.find_elements_by_xpath("./li"):
                #print(i.text)
                try:
                    #Checking for inmail message - if found then break the loop and moving to next connection - else Normal message
                    try:
                        inputdiv = driver.find_element_by_xpath("//*[@placeholder='Subject (required)']")
                        print("--Not Connected--")
                        sleep(2)
                        break
                    except:
                        sleep(2)
                        pass
                    
                    # userName = i.find_element_by_tag_name("address")
                    #print(userName.text, len(userName.text))
                    # if userName.text == "You":
                    #print("--Some Message Sent By You, Searching Invitation Message... Wait...--")
                    
                    #Retriving 1 msg
                    sleep(2)
                    article = i.find_element_by_tag_name("article")
                    sleep(2)
                    msg = article.find_element_by_xpath("./div[2]")

                    #Checking msg is "I have a great job offer for you" or not
                    if "I have a great job offer for you" in msg.text:
                        print("--Invitation Message Found--")

                        #If Msg found enter Reply msg
                        textArea = driver.find_element_by_xpath("//*[@class='flex-grow-1 overflow-y-auto']")
                        textArea = textArea.find_element_by_tag_name("textarea")
                        textArea.click()
                        sleep(2)
                        textArea.send_keys(ReplyMsg)
                        
                        #Click on send
                        sleep(2)
                        send = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml4']")
                        send.click()
                        print("--Reply Message sent successfully--")
                        break
                except:
                    #For ignoring 1 element of ul - li
                    sleep(2)
                    print("--Invitation message is searching.--")
                    #traceback.print_exc()
            #break
            print("Count : ", count)
            if count < Limit:
                count += 1
            else:
                print("Limit is reached... Reply Message is stopped")
                break
            
    except:
        print("Error Occured...")
        traceback.print_exc()

LSN_Reply()

'''
Output:
Input$ python LSN_Reply.py sumi@codemarket.io Codemarket.123 "We have multiple job openings in MERN stack, Python, ML/AI, Designer UI-UX, and IOS/Android mobile App Development. The following questions help to match the opportunity  1. What is the timeline for when you would like to join?  2. What is your current salary/stipend?  3. What is your expected salary/stipend?  4. Send your resume here on LinkedIn chat  5. What is your skill set?  6. what is your whatsapp?  To move forward please answer the above questions. Interview takes place on WhatsApp." 7


Current Url : https://www.linkedin.com/feed/
Login...
Redirected to Linkedin Sales Navigator Inbox Page.
2
--Invitation message is searching.--
--Invitation Message Found--
--Reply Message sent successfully--
Count :  1
6
--Invitation message is searching.--
Count :  2
2
--Invitation message is searching.--
--Invitation Message Found--
--Reply Message sent successfully--
Count :  3
2
--Not Connected--
Count :  4
2
--Not Connected--
Count :  5
3
--Invitation message is searching.--
Count :  6
4
--Invitation message is searching.--
--Invitation Message Found--
--Reply Message sent successfully--
Count :  7
Limit is reached... Reply Message is stopped
'''