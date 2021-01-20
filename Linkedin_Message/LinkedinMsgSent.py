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
# from selenium.webdriver import ActionChains

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)

#Taking Input
# EmailId = 'donnybegins@gmail.com'
EmailId = sys.argv[1]

# Password = 'myaccount'
Password = sys.argv[2]

# UserName = "Sunny Tarawade"
#UserName = sys.argv[3]

# MessageSend = 'Thanks :)'
MessageSend = sys.argv[3]

#Sign in into linked account
driver.get("https://www.linkedin.com/login")
driver.find_element_by_id("username").send_keys(EmailId)
password = driver.find_element_by_id("password")
sleep(2)
password.send_keys(Password)
password.send_keys(Keys.RETURN)
print("Login...")

# divelement = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]") 

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


#Finding 
try:
    # Checking chat window in open or not
    chatWindow()
    sleep(2)

    #all chat message div element
    allChatMessage = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/section/div/div[1]")
    print(len(allChatMessage.find_elements_by_xpath("./div")))

    #Setting flag = 0  for finding user name
    Flag = 0

    #Going throw loop to find user
    for x in range(len(allChatMessage.find_elements_by_xpath("./div"))):
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

        #Finding send button
        send = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/div[1]/form/footer/div[2]/div/button")
        send.click()
        print("Message Sent...")

        #For closing window
        miniWindow = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[2]/header/section[2]/button[2]")
        miniWindow.click()

    # if(Flag == 0):
    #     print("Name Not Found ! Enter correct Name.")
    #     //*[@id="msg-overlay"]/div[1]/section/div/div[1]/div[1]/div/div[2]/div/div[1]/h4
except:
    print("Error Occured...")
    traceback.print_exc()

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