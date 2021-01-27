from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import random
import sys
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection

Email_id = sys.argv[1]
Password = sys.argv[2]
sleeps = [2,3,4]
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
        time.sleep(5)
    # otp = int(input("Please enter the OTP recieved at registered mobile number: "))
    # driver.current_url
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otp)
    submit_otp.send_keys(Keys.RETURN)
    my_db.linkedin_otp.drop()
        
def chat_scroll():
    chats = chat_list.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   msg-overlay-list-bubble__convo-item--v3']")
    chat_len = len(chats)
    for l in chats :
        driver.execute_script("arguments[0].scrollIntoView();", l)
        time.sleep(1)
        chat_check = chat_list.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   msg-overlay-list-bubble__convo-item--v3']")
#         print(len(chat_check))
    if len(chat_check) > chat_len:
        chat_scroll()
    return chat_check



chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument('--disable-dev-shm-usage')

# PATH= r"/usr/local/bin/chromedriver"
PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=chrome_options)


driver.get("https://www.linkedin.com/login")
driver.find_element_by_id("username").send_keys(Email_id)
password = driver.find_element_by_id("password")
time.sleep(random.choice(sleeps))
password.send_keys(Password)
password.send_keys(Keys.RETURN)

if 'https://www.linkedin.com/checkpoint' in driver.current_url:
    otp()
print('Login...')
    
chat_list = driver.find_element_by_xpath("//div[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
# chat_list
chat_container = chat_scroll()
soup1 = BeautifulSoup(driver.page_source, 'html.parser')
chats = soup1.find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item msg-overlay-list-bubble__convo-item--v3"})

for enu,chat in enumerate(chats):
    chat = chats[enu].find('mark', attrs={"class":"msg-conversation-card__unread-count"})
    if chat:
        print("New Message")
        chat_container[enu].send_keys(Keys.RETURN)
        time.sleep(random.choice(sleeps))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        chat_box = soup.find('div', {"class":"msg-overlay-conversation-bubble"})
        
        conversation_list = chat_box.find('ul', {"class":"msg-s-message-list-content list-style-none full-width"})
        time.sleep(random.choice(sleeps))
        conversation = conversation_list.find_all('li')
        time.sleep(random.choice(sleeps))
        container = chat_box.find('h4')
        name = container.find('a').text.strip()
        # print(name)
        first_name = name.split(' ')[0]
        last_name = name.split( ' ')[1]
        if len(conversation) < 4:
            link = conversation[0].find_all('a')
            link = link[1]['href']

            profile_link= "https://www.linkedin.com"+link
            # print(profile_link)
        
        conversation.reverse()
        for num,messages in enumerate(conversation):
            # print("ATTEMPT",num)
            if messages.p is None:
                # print("NO message")
                continue
            if messages.find('a')is None:
                # print("NO LINK")
                continue
            name_ = messages.find_all('a')
            name1 = name_[1].text.strip()
            link = messages.find('a')['href']
            msg = messages.p.text
            if name1 == name:
                link = messages.find('a')['href']
                profile_link= "https://www.linkedin.com"+link
                # print(profile_link)
            if name1 != name:
                my_link = messages.find('a')['href']
                link = messages.find('a')['href']
                msg = messages.p.text
#                 print(name1)
#                 print(my_link)
                if msg == 'I have a great job opportunity for you' or msg == 'I have a great job opportunity for you.':
                    print("Replying")

                    message = f"www.soozzi.com/job?linkedinurl=={profile_link}&&firstname={first_name}&&lastname={last_name}"
                    reply = driver.find_element_by_xpath("//div[@aria-label='Write a message…']")
                    time.sleep(random.choice(sleeps))
                    reply.send_keys(message)
                    send_reply = driver.find_element_by_xpath("//button[@type='submit']")
                    time.sleep(random.choice(sleeps))
                    send_reply.send_keys(Keys.RETURN)

                    close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                    time.sleep(random.choice(sleeps))
                    close_chat.send_keys(Keys.RETURN)
                    print("Replied")
                    time.sleep(random.choice(sleeps))
#                     break
                else: 
#                     print("ELSE")
                    close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                    time.sleep(random.choice(sleeps))
                    close_chat.send_keys(Keys.RETURN)
                    time.sleep(random.choice(sleeps))
                break
             
#                     print("ELSE")
        
        try:
            close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
            time.sleep(random.choice(sleeps))
            if close_chat:
                
                close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                time.sleep(random.choice(sleeps))
                close_chat.send_keys(Keys.RETURN)
                time.sleep(random.choice(sleeps)) 
        except:
            pass
#         break