from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
import requests
import sys
import time
import random
import traceback
from time import sleep
import urllib.parse
import pymongo
import ast
# from selenium.webdriver import ActionChains

#Input : python LinkedinMsgSent.py email@gmail.com password HelloWorld "['https://www.linkedin.com/in/nooras-fatima-ansari-2542b3171/', 'https://www.linkedin.com/in/daniel-piersch-ba003b71/'] 0

print("Script Started running...")

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

#Taking Input
# EmailId = 'donnybegins@gmail.com'
EmailId = sys.argv[1]

# Password = 'myaccount'
Password = sys.argv[2]

# UserName = "Sunny Tarawade"
#UserName = sys.argv[3]

# MessageSend = 'Thanks :)'
MessageSend = sys.argv[3]

url = ast.literal_eval(sys.argv[4])

Limit = int(sys.argv[5])

print(EmailId, " ", Password, " ", MessageSend, " ", url, " ", Limit)

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
            otp = data[0]['OTP']
            # print("otp is: ",otp)
            otp_collection.update_many( 
            {"linkedin_login_url":EmailId, "Status":"OTP updated"}, 
            { "$set":{ "Status":"Login complete" }},)
            print("Found OTP")
            break
        print("Waiting for correct OTP...")
        sleep(15)
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otp)
    submit_otp.send_keys(Keys.RETURN)

    if driver.current_url == 'https://www.linkedin.com/checkpoint/challenge/verify':
        print("Dropping collection")
        sleep(2)
        otp_collection.drop()
        print("Incorrect OTP. Enter correct otp.")
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
        LinkedInMsg()
    print("No return...")
  
#For checking window is closed or not
def chatWindowClose():
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

def LinkedInMsg():

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

    if "https://www.linkedin.com/checkpoint" in driver.current_url:
        print("OTP...")
        value = otp()
        if value == True:
            print("Redirected to Feed Page.")
        else:
            print("Something went wrong!!")

    if 'https://www.linkedin.com/feed' in driver.current_url:
        print("Login...")
    else:
        print("Something is wrong!! Try again!! Network Problem!!")
        print(driver.current_url)

    #Finding 
    try: 
        if Limit == 0 and url:
            for x in url:
                driver.get(x)
                sleep(2)
                chatWindowClose()
                try:
                    sleep(2)
                    element = "//*[@class='display-flex justify-flex-end align-items-center']/div/div[1]/a"
                    btn = driver.find_element_by_xpath(element)
                    #print(btn.text)
                    sleep(2)
                    if btn.text == "Message":
                        sleep(2)
                        btn.click()
                        sleep(2)
                        msg = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/div[3]/div/div/div/p")
                        msg.click()
                        sleep(2)
                        msg.send_keys(MessageSend)
                        sleep(2)
                        send = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/footer/div[2]/div/button")
                        send.click()
                        print("Message Sent...")
                        smallBox = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/header/section[2]/button[2]")
                        smallBox.click()
                        print("Connection Found")
                except:
                    print("Connection is not connected")
        elif Limit > 0 and not len(url):
            chatWindowClose()
            sleep(2)
            driver.get("https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH")
            sleep(3)
            #divelement = driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div[2]/ul")
            divelement = driver.find_element_by_xpath("//*[@class='pv2 artdeco-card ph0 mb2']/ul")
            sleep(2)
            #Setting Limit
            TotalMsgLength = len(divelement.find_elements_by_xpath("./li"))
            if Limit > TotalMsgLength:
                finalLimit = TotalMsgLength
            else:
                finalLimit = Limit

            #Going through all loop
            for x in range(finalLimit):
                y = "//*[@class='pv2 artdeco-card ph0 mb2']/ul/li[" + str(x+1) + "]/div/div/div[3]/button"
                #y = "/html/body/div[8]/div[3]/div/div[2]/div/div[2]/div/div[2]/ul/li[" + str(x+1) + "]/div/div/div[3]/button"
                btn = driver.find_element_by_xpath(y)
                sleep(2)
                print(btn.text)
                if btn.text == "Message":
                    btn.click()
                    sleep(2)
                    
                    msg = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/div[3]/div/div/div/p")
                    #print(msg) #//*[@id="ember749"]/div/div[1]/div[1]/p
                    msg.click()
                    msg.send_keys(MessageSend)
                    print(MessageSend, len(MessageSend))
                    sleep(2)
                    
                    send = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/footer/div[2]/div/button")
                    send.click()
                    #print(send.click())
                    print("Message Sent...")
                    sleep(1)

                    smallBox = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/header/section[2]/button[2]")
                    smallBox.click()
            print("Script Stopped running...")
    except:
        print("Error Occured...")
        traceback.print_exc()

LinkedInMsg()

#Msg sent from chat window

#For Opening chat window
# def chatWindow():
#     try:
#         sleep(2)
#         chatOpen = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/div")
#         print("Chat Window is already Opened...")
#     except:
#         sleep(2)
#         print("Chat Window is closed...")
#         chatClose = driver.find_element_by_xpath("(//*[@id='msg-overlay']/div[1]/header/section[1])")
#         chatClose.click()
#         print("Chat Window Opened...")
  
# Checking chat window in open or not
#chatWindow()
#all chat message div element
# allChatMessage = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/section/div/div[1]")
# print(len(allChatMessage.find_elements_by_xpath("./div")))

#Going through loop to find user
# for x in range(finalLimit):
#     divTag = "//*[@id='msg-overlay']/div[1]/section/div/div[1]/div[" + str(x+1) + "]/div/div[2]/div/div[1]/h4"
#     #print(divTag)
#     sleep(2)
#     UserDiv = driver.find_element_by_xpath(divTag)
#     print("Name : ", UserDiv.text)

#     #if UserDiv.text == UserName:
#     #Flag = 1
#     #print("Name Found...")

#     #Clicking on user name
#     UserDiv.click()

#     #Finding p tag to click and enter msg
#     sleep(2)
#     pTagMsg = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/div[3]/div/div/div/p")
#     #print(pTagMsg) 
#     sleep(2)
#     pTagMsg.click()
#     pTagMsg.send_keys(MessageSend)
#     print("Ptag : ", pTagMsg, MessageSend)
#     #Finding send button
#     sleep(2)
#     send = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/footer/div[2]/div/button")
#     send.click()
#     print("Send : ", send)
#     print("Message Sent...")

#     #For closing window
#     miniWindow = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/header/section[2]/button[2]")
#     miniWindow.click()
#     print("Mini Window: ", miniWindow)

'''
Input: python LinkedinMsgSent.py email@gmail.com password "Message" 2
'''