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

#Taking Input
Email_id = sys.argv[1]

Password = sys.argv[2]

ReplyMsg = sys.argv[3]

Limit = int(sys.argv[4])

sleeps = [2,3,4]
#Setting Chrome browser
chrome_options = Options()
# chrome_options.add_argument(" — incognito")
# chrome_options.add_argument("--window-size=1920,1200")
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")

PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
# PATH= r"/usr/local/bin/chromedriver"
chrome_options = Options()
driver = webdriver.Chrome(PATH,options=chrome_options)


def otp():
    client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    time.sleep(random.choice(sleeps))
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
        time.sleep(random.choice(sleeps))
    # otp = int(input("Please enter the OTP recieved at registered mobile number: "))
    # driver.current_url
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otp)
    submit_otp.send_keys(Keys.RETURN)
    my_db.linkedin_otp.drop()

driver.get("https://www.linkedin.com/login")
driver.find_element_by_id("username").send_keys(Email_id)
password = driver.find_element_by_id("password")
time.sleep(random.choice(sleeps))
password.send_keys(Password)
password.send_keys(Keys.RETURN)

if 'https://www.linkedin.com/checkpoint' in driver.current_url:
    otp()
print('Login...')

if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit' or "login-submit" in driver.current_url:
        print("Incorrect login details")

if 'https://www.linkedin.com/checkpoint/lg/login?errorKey=challenge_global_internal_error' in driver.current_url:
    print("Sorry something went wrong. Please try again later")

print("Redirected to Linkedin Sales Navigator Inbox Page.")
driver.get("https://www.linkedin.com/sales/inbox")

sleep(10)

ul = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
count = 1

chats = ul.find_elements_by_xpath("./li")

ul = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
count = 1

chats = ul.find_elements_by_xpath("./li")

for enu,x in enumerate(chats):
    print('OPENING NEW CHAT')
#     print("ENUMERATING:",enu)
    #Selection 1 connection 
    time.sleep(random.choice(sleeps))
    a = x.find_element_by_tag_name('a')
    # print(a)
    a.click()
    time.sleep(random.choice(sleeps))

    #Chat Inbox
    inbox = driver.find_element_by_xpath("//*[@class='flex flex-column flex-grow-1 flex-shrink-zero justify-flex-end ember-view']/ul")
    print(len(inbox.find_elements_by_xpath("./li")))
    for i in inbox.find_elements_by_xpath("./li"):
        try:
                         #Checking for inmail message - if found then break the loop and moving to next connection - else Normal message
            try:
                inputdiv = driver.find_element_by_xpath("//*[@placeholder='Subject (required)']")
                print("--Not Connected--")
                time.sleep(random.choice(sleeps))
                break
            except:
                sleep(2)
                pass
        #     sleep(2)
#             print(i.text)
        #         break


            article = i.find_element_by_tag_name("article")
            time.sleep(random.choice(sleeps))
            msg = article.find_element_by_xpath("./div[2]")

            #Checking msg is "I have a great job offer for you" or not
            if "I have a great job opportunity for you" in msg.text:
                print("--Invitation Message Found--")

                first_name = x.text.replace('\n', ' ').strip().split(' ')[0]
                last_name = x.text.replace('\n', ' ').strip().split(' ')[1]

                #Getting profile url by navigating into the profile


                right_rail = driver.find_element_by_xpath("//div[@class='inbox__right-rail-container conversation-insights full-height flex flex-column ember-view']")
                profile = right_rail.find_element_by_xpath("//div[@class='ml1 artdeco-entity-lockup__content ember-view']")
                profile.click()
                time.sleep(random.choice(sleeps))
                
                main_window = driver.window_handles[0]
                LSN_profile = driver.window_handles[1]
                driver.switch_to.window(window_name=LSN_profile)
                
                driver.find_element_by_xpath("//li-icon[@type='ellipsis-horizontal-icon']").click()
                time.sleep(random.choice(sleeps))
                
                linkedin_profile = driver.find_element_by_xpath("//div[@data-control-name='view_linkedin']").click()
                time.sleep(random.choice(sleeps))

                linkedin_profile = driver.window_handles[2]
                driver.switch_to.window(window_name=linkedin_profile)
                time.sleep(random.choice(sleeps))
                linkedin_url = driver.current_url
                print(linkedin_url)
                driver.close()

                driver.switch_to.window(window_name=LSN_profile)
                driver.close()

                driver.switch_to.window(window_name=main_window)
                time.sleep(random.choice(sleeps))

                #Getting name



                #If Msg found enter Reply msg
                textArea = driver.find_element_by_xpath("//*[@class='flex-grow-1 overflow-y-auto']")
                textArea = textArea.find_element_by_tag_name("textarea")
                textArea.click()
                time.sleep(random.choice(sleeps))
                textArea.send_keys(ReplyMsg) 

                #Click on send
                time.sleep(random.choice(sleeps))
                send = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml4']")
                send.click()

                message = f"www.soozzi.com/job?linkedinurl={linkedin_url}&firstname={first_name}&lastname={last_name}"
                textArea.send_keys(message) 
                time.sleep(random.choice(sleeps))
                send = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml4']").click()


                print("--Reply Message sent successfully--")
                break
        except:
            #For ignoring 1 element of ul - li
            time.sleep(random.choice(sleeps))
            print("--Invitation message is searching.--")
    
    if count < Limit:
                count += 1
    else:
        print("Limit is reached... Reply Message is stopped")
        break
    



