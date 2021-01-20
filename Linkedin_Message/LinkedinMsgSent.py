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

driver = webdriver.Chrome()
chrome_options = Options()

#Taking Input
# EmailId = 'donnybegins@gmail.com'
EmailId = sys.argv[1]

# Password = 'myaccount'
Password = sys.argv[2]

# UserName = "Sunny Tarawade"
UserName = sys.argv[3]

# MessageSend = 'Thanks :)'
MessageSend = sys.argv[4]

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
        #Finding user name
        if UserDiv.text == UserName:
            print("Name : ", UserDiv.text)
            Flag = 1
            print("Name Found...")

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
            break

    if(Flag == 0):
        print("Name Not Found ! Enter correct Name.")
    #     //*[@id="msg-overlay"]/div[1]/section/div/div[1]/div[1]/div/div[2]/div/div[1]/h4
except:
    print("Error Occured...")
    traceback.print_exc()

'''
Output :
$ python LinkedinMsgSent.py youremail@gmail.com yourpassword "Kiran Virani" "Thanks :)"
Login...
Chat Window is already Opened...
15
Name :  Kiran Virani
Name Found...
Message Sent...

'''