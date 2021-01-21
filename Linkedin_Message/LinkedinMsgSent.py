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
# from selenium.webdriver import ActionChains

print("Script Started running...")

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

#Taking Input
# EmailId = 'donnybegins@gmail.com'
EmailId = sys.argv[1]

# Password = 'myaccount'
Password = sys.argv[2]

# UserName = "Sunny Tarawade"
#UserName = sys.argv[3]

# MessageSend = 'Thanks :)'
MessageSend = sys.argv[3]

Limit = int(sys.argv[4])
print(EmailId, " ", Password, " ", MessageSend, " ", Limit)

#DB connection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
otp_collection = db.OTP_linkedin #collection


#challenge/AgFXl5GhM3Yu-AAAAXcjYRVOXQ1W6sE0jHWKUPxYk9s2SHi_OVXAqE81cqRKJHmuy7W_ke3htu1rCcwgsLAHzMmD2TScSQ?ut=1vd69TEFY-M9A1

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

#For Opening chat window
def chatWindow():
    try:
        sleep(2)
        chatOpen = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/div")
        print("Chat Window is already Opened...")
    except:
        sleep(2)
        print("Chat Window is closed...")
        chatClose = driver.find_element_by_xpath("(//*[@id='msg-overlay']/div[1]/header/section[1])")
        chatClose.click()
        print("Chat Window Opened...")

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
        # Checking chat window in open or not
        chatWindow()
        sleep(2)

        #all chat message div element
        allChatMessage = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/section/div/div[1]")
        print(len(allChatMessage.find_elements_by_xpath("./div")))

        #Setting Limit
        TotalMsgLength = len(allChatMessage.find_elements_by_xpath("./div"))
        if Limit > TotalMsgLength:
            finalLimit = TotalMsgLength
        else:
            finalLimit = Limit

        #Going throw loop to find user
        for x in range(finalLimit):
            divTag = "//*[@id='msg-overlay']/div[1]/section/div/div[1]/div[" + str(x+1) + "]/div/div[2]/div/div[1]/h4"
            #print(divTag)
            sleep(2)
            UserDiv = driver.find_element_by_xpath(divTag)
            print("Name : ", UserDiv.text)

            #if UserDiv.text == UserName:
            #Flag = 1
            #print("Name Found...")

            #Clicking on user name
            UserDiv.click()

            #Finding p tag to click and enter msg
            sleep(2)
            pTagMsg = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/div[3]/div/div/div/p")
            #print(pTagMsg) 
            sleep(2)
            pTagMsg.click()
            pTagMsg.send_keys(MessageSend)
            print("Ptag : ", pTagMsg)
            #Finding send button
            send = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/footer/div[2]/div/button")
            send.click()
            print("Send : ", send)
            print("Message Sent...")

            #For closing window
            miniWindow = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/header/section[2]/button[2]")
            miniWindow.click()
            print("Mini Window: ", miniWindow)
        print("Script Stopped running...")
        # if(Flag == 0):
        #     print("Name Not Found ! Enter correct Name.")
        #     //*[@id="msg-overlay"]/div[1]/section/div/div[1]/div[1]/div/div[2]/div/div[1]/h4
    except:
        print("Error Occured...")
        traceback.print_exc()

LinkedInMsg()


'''
Output :
$ python LinkedinMsgSent.py youremailid@gmail.com yourpass "Thanks For connecting"
Login...
Chat Window is already Opened...
2
Name :  Donny Koay
Message Sent...
Name :  Nooras Fatima Ansari
Message Sent...

'''