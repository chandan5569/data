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

# New Input : python LinkedinMsgSent.py <Email> <Password> <Keyword> <Geography> <Relationship in quotes separted by spaces> <MessageSend> <Now Empty list for url> <Limit(count)>

# New Input : python LinkedinMsgSent.py email@gmail.com password python India "2 3" "I have a great job offer for you" "" 5

# Input : python LinkedinMsgSent.py email@gmail.com password HelloWorld "['https://www.linkedin.com/in/nooras-fatima-ansari-2542b3171/', 'https://www.linkedin.com/in/daniel-piersch-ba003b71/'] 0

print("Script Started running...")

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument("--window-size=1920,1200");
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options)

#Taking Input
# EmailId = 'donnybegins@gmail.com'
EmailId = sys.argv[1]

# Password = 'myaccount'
Password = sys.argv[2]

# UserName = "Sunny Tarawade"
#UserName = sys.argv[3]

# KeyWord = "python"
KeyWord = sys.argv[3]

# Geography = "India"
Geography = sys.argv[4]

# Relationship = "2 3"
Relationship = sys.argv[5]
Relationship = Relationship.split() #Converting string into list Relationship -> ['2', '3']

# Subject = "Job Offer"
#Subject = sys.argv[6]

# MessageSend = 'Thanks :)'
MessageSend = sys.argv[6]

url = sys.argv[7]
url = url.split()

Limit = int(sys.argv[8])

#print(EmailId, " ", Password, " ", KeyWord, " ", Geography, " ", Relationship, " ",  MessageSend, " ", url, " ", Limit)

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

    print("Current Url : " + driver.current_url)
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
        # Python Script That Sends Messages To 2nd & 3rd Degree Connections (Geography +) In Linkedin Sales Navigator
        if KeyWord and Geography and Relationship and MessageSend and Limit:

            #Linkedin Sales Navigator
            driver.get('https://www.linkedin.com/sales/homepage')

            #KeyWord
            sleep(3)
            searchBar = driver.find_element_by_xpath("//*[@id='global-typeahead-search-input']")
            sleep(3)
            searchBar.click()
            sleep(3)
            searchBar.send_keys(KeyWord)
            sleep(2)
            searchBar.send_keys(Keys.RETURN)
            print("-- Keyword is selected --")

            #Geography and Relationship
            ul = driver.find_element_by_xpath("//*[@class='search-filter__list collapsible-container is-expanded ember-view']")
            for x in range(1,len(ul.find_elements_by_xpath("./li"))-1):
                divLi = driver.find_element_by_xpath("//*[@class='search-filter__list collapsible-container is-expanded ember-view']/li[" + str(x+1) + "]/div/div/div/div/div")
                #print(divLi.text)

                #For Geaography
                if divLi.text == "Geography":
                    buttonLi = driver.find_element_by_xpath("//*[@class='search-filter__list collapsible-container is-expanded ember-view']/li[" + str(x+1) + "]/div/div/div/div/button")
                    buttonLi.click()
                    sleep(2)
                    inputLi = driver.find_element_by_xpath("//*[@class='search-filter__list collapsible-container is-expanded ember-view']/li[" + str(x+1) + "]/div/div/div[2]/input")
                    inputLi.send_keys(Geography)
                    #inputLi.send_keys('India')
                    sleep(2)
                    inputLiOl = driver.find_element_by_xpath("//*[@class='search-filter-typeahead__list overflow-y-auto']/li[1]/button")
                    inputLiOl.click() 
                    sleep(2)
                    print("-- Geography Selected --")
                    
                #For relationship
                if divLi.text == "Relationship":
                    buttonLi = driver.find_element_by_xpath("//*[@class='search-filter__list collapsible-container is-expanded ember-view']/li[" + str(x+1) + "]/div/div/div/div/button")
                    buttonLi.click()
                    sleep(2)
                    inputLiOl = driver.find_element_by_xpath("//*[@class='search-filter-typeahead__list overflow-y-auto']")
                    for r in Relationship:
                        for li in range(len(inputLiOl.find_elements_by_xpath("./li"))):
                            buttonRelationship = driver.find_element_by_xpath("//*[@class='search-filter-typeahead__list overflow-y-auto']/li["+str(li+1)+"]/button")
                            if str(r) in buttonRelationship.text:
                                buttonRelationship.click()
                                sleep(2)
                                print("-- Relationship Selected --")
                                #print("yess", buttonRelationship.text)
                                break

            #Invitation send
            ol = driver.find_element_by_xpath("//*[@class='search-results__result-list']")
            sleep(2)
            try:
                count = 0
                page = 2 #bydafault page 1 is loaded
                while count < Limit:
                    print("Invitation sending is in progress...")

                    #Scroll Length
                    length = driver.execute_script("return document.documentElement.scrollHeight")
                    scrollLength = 180
                    driver.execute_script("window.scrollTo(0, 0)")

                    #Going through all tab of connection profile
                    for x in ol.find_elements_by_xpath("./li"):
                        #print(x)
                        try:
                            #3Dots
                            y = x.find_element_by_xpath("div[2]/div/div/div/article/section[1]/div[2]/ul/li/div/div[2]")
                            y.click()
                            sleep(2)

                            div = x.find_element_by_xpath("div[2]/div/div/div/article/section[1]/div[2]/ul/li/div/div[2]/div/div/div/div/ul")
                            #print(len(div.find_elements_by_xpath("./li")))

                            #Going through all list options
                            for m in div.find_elements_by_xpath("./li"):
                                #print("Hii")
                                #print(m.text)

                                #For connect
                                if m.text == "Connect":
                                    try:
                                        #print("If connect")
                                        m.click()
                                        sleep(2)

                                        #textArea for wrirting note
                                        textArea = driver.find_element_by_xpath("//*[@class='ember-text-area ember-view']")
                                        textArea.click()
                                        textArea.send_keys(MessageSend)
                                        sleep(3)

                                        #Click on send
                                        buttonSend = driver.find_element_by_xpath("//*[@class='button-primary-medium connect-cta-form__send']")
                                        buttonSend.click()
                                        sleep(2)

                                        print("--- Send Invitation successfully(Tab) ---")
                                        break
                                    except:
                                        print("--Error while sending invitation from tab--")

                                #For pending        
                                elif m.text == "Pending":
                                    y.click() #Clciking on again to see below tab's button
                                    print("-- Invitation is pending --")
                                    break

                                #For View profile
                                elif m.text == "View profile":
                                    #print("Else View Profile")
                                    first_link = m.find_element_by_tag_name('a')
                                    
                                    #Save the window opener (current window)
                                    main_window = driver.current_window_handle
                                    
                                    #Open the link in a new tab by sending key strokes on the element
                                    first_link.send_keys(Keys.CONTROL + Keys.RETURN)
                                    sleep(2)

                                    # Switch tab to the new tab, which we will assume is the next one on the right
                                    driver.switch_to.window(driver.window_handles[1])
                                    sleep(4)

                                    #view profile dots 
                                    viewProfileDots = driver.find_element_by_xpath("(//*[@class='profile-topcard-actions flex align-items-center mt2']/div)[last()]")
                                    viewProfileDots.click()
                                    sleep(2)

                                    #view profile list options
                                    viewProfileConnect = viewProfileDots.find_element_by_xpath("div/div/div/div/ul")
                                    for x in viewProfileConnect.find_elements_by_xpath("./li"):
                                        try:
                                            #print("Tab")
                                            #For connect
                                            if x.text == "Connect":
                                                x.click()
                                                sleep(2)

                                                textArea = driver.find_element_by_xpath("//*[@class='ember-text-area ember-view']")
                                                textArea.click()
                                                sleep(2)
                                                textArea.send_keys(MessageSend)
                                                sleep(3)

                                                buttonSend = driver.find_element_by_xpath("//*[@class='button-primary-medium connect-cta-form__send']")
                                                buttonSend.click()
                                                sleep(2)
                                                print("--- Send Invitation successfully ---")
                                                break

                                            #For pending
                                            elif x.text == "Pending":
                                                print("--- Invitation is pending ---")
                                                break
                                        except:
                                            print("--- Send Invitation error or Invitation is pending ---")
                                            
                                    #Close the new tab
                                    driver.close()

                                    #Switch back to old tab
                                    driver.switch_to.window(main_window)
                                    break
                                # if m.text == "Message":
                                #     print(m.text)
                                #     m.click()
                                #     sleep(2)

                                #     #Subject
                                #     formInput1 = driver.find_element_by_xpath("//*[@class='compose-form__subject-field flex-none ember-text-field ember-view']")
                                #     formInput1.click()
                                #     sleep(2)
                                #     formInput1.send_keys(Subject)
                                #     # formInput1.send_keys('Job Offer')
                                #     sleep(2)

                                #     #MessageSend
                                #     formInput2 = driver.find_element_by_xpath("//*[@class='flex flex-column flex-grow-1 overflow-hidden']/section[1]/textarea")
                                #     formInput2.click()
                                #     sleep(2)
                                #     formInput2.send_keys(MessageSend)
                                #     # formInput2.send_keys('I have a great job offer for you')
                                #     sleep(2)
                                #     send = driver.find_element_by_xpath("//*[@class='flex flex-column flex-grow-1 overflow-hidden']/section[2]/span/button")
                                #     send.click()
                                #     sleep(2)

                                #     print("--- One Msg Sent Succefully ---")

                            driver.execute_script("window.scrollTo(0, " + str(scrollLength) + ")")
                            if scrollLength + 180 < length:
                                scrollLength += 180
                        except:
                            print("-- Unsuccessfull, Invitation Can't send --")

                        print("Count : ", count)
                        if count + 1 < Limit:
                            count += 1
                        else:
                            break

                    if count +1 < Limit:
                        link = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded=102713980&keywords=python&logHistory=false&page="+ str(page)+ "&preserveScrollPosition=false&relationship=S%2CO&rsLogId=770008140&searchSessionId=jh8CsJ15Sl2Qx4QQTraN7g%3D%3D"
                        driver.get(link)
                        print("Page : " + Page)
                        page += 1
                    else:
                        print("Limit Is Reached... Invitation Send Stopped...")
                        break

            except:
                    print("Error!! In Sending Invitation...")
                    traceback.print_exc()

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
        elif Limit > 0 and not len(url) and (not Geography):
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