from selenium import webdriver
from bs4 import BeautifulSoup
import os,random,time,argparse
from bs4 import BeautifulSoup as bs 
import csv
import re


parser = argparse.ArgumentParser()
parser.add_argument('email', help='linkedin email')
parser.add_argument('password', help='linkedin password')
args = parser.parse_args()

browser = webdriver.Chrome('/home/saurabh/linkedin/chromedriver.exe')
browser.get('https://www.linkedin.com')
browser.maximize_window()

email_element = browser.find_element_by_id("session_key")
email_element.send_keys(args.email)

pass_element = browser.find_element_by_id("session_password")
pass_element.send_keys(args.password)
pass_element.submit()

print ("success! Logged in, Bot starting")
browser.implicitly_wait(3)

browser.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

total_height = browser.execute_script("return document.body.scrollHeight")
while True:
     # Scroll down to bottom
     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     # Wait to load page
     time.sleep(random.uniform(2.5, 4.9))
     # Calculate new scroll height and compare with total scroll height
     new_height = browser.execute_script("return document.body.scrollHeight")
     if new_height == total_height:
        break
     last_height = new_height

page = bs(browser.page_source, features="html.parser")
content = page.find_all('a', {'class':"mn-connection-card__link ember-view"})

mynetwork = []
for contact in content:
    mynetwork.append(contact.get('href'))
print(len(mynetwork), " connections")


my_network_emails = []
linkedin_link = []
# Connect to the profile of all contacts and save the email within a list
for contact in mynetwork:
    browser.get("https://www.linkedin.com" + contact + "detail/contact-info/")
    browser.implicitly_wait(3)
    contact_page = bs(browser.page_source, features="html.parser")
    name = contact_page.find_all('a',href=re.compile("linkedin.com/in/"))
    #print(name)
    content_contact_page = contact_page.find_all('a',href=re.compile("mailto"))
    for contact in content_contact_page:
        print("[+]", contact.get('href')[7:])
        my_network_emails.append(contact.get('href')[7:])
    # wait few seconds before to connect to the next profile
    for name in name:
        print(name.get('href'))
        linkedin_link.append(name.get('href'))
    time.sleep(random.uniform(0.5, 1.9))

# browser.get("https://www.linkedin.com" + contact + "detail/contact-info/")

# content_contact_page = contact_page.find_all('a',href=re.compile("mailto"))
# for contact in content_contact_page:
#    print("[+]", contact.get('href')[7:])
#    my_network_emails.append(contact.get('href')[7:])

with open(f'network_emails.csv', 'w') as f:
   writer = csv.writer(f)
   email=0
   while email<len(my_network_emails):
        writer.writerow([my_network_emails[email],linkedin_link[email]])
        email+=1