from selenium import webdriver
from bs4 import BeautifulSoup
import os,random,time,argparse
from bs4 import BeautifulSoup as bs 
import csv
import re
import bs4


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


my_network_emails = ["Email"]
linkedin_link = ["Linkedin_link"]
exp_deatails1 = ["Experience"]
edu_details1 = ["Education"]
name5 = ["Name"]
# Connect to the profile of all contacts and save the email within a list
for contact in mynetwork:
    browser.get("https://www.linkedin.com" + contact)
    browser.implicitly_wait(3)
    src = browser.page_source
    soup = bs4.BeautifulSoup(src,'html.parser')
    name_div = soup.find('div',{'class':'flex-1 mr5'})
    name_loc = name_div.find_all('ul')
    name = name_loc[0].find('li').get_text().strip()
    print(name)
    name5.append(name)

#exp section
    exp_deatails = []
    exp = soup.find('section',{'id':"experience-section"})    
    if exp is not None:
        exp1 = exp.find('ul')
        li_tag = exp1.find('div')
        a_tag = li_tag.find('a')
        job_title = a_tag.find('h3').get_text().strip()
        exp_deatails.append(job_title)
        company_name = a_tag.find_all('p')[1].get_text().strip()
        exp_deatails.append(company_name)
        j_date = a_tag.find_all('h4')[0].find_all('span')[1].get_text().strip()
        exp_deatails.append(j_date)
        e_date = a_tag.find_all('h4')[1].find_all('span')[1].get_text().strip()
        exp_deatails.append(e_date)
        exp_deatails1.append(exp_deatails)
    else:
        exp_deatails1.append("Detail Not Found!")
    #education section
    edu_details = []
    edu_section = soup.find('section',{'id','education-section'})
    if edu_section:
        clg_name = edu_section.find('h3').get_text().strip()
        edu_details.append(clg_name)
        degree_name = edu_section.find('p',{'class':"pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"}).find_all('span')[1].get_text().strip()
        edu_details.append(degree_name)
        stream_name = edu_section.find('p',{'class':"pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"}).find_all('span')[1].get_text().strip()
        edu_details.append(stream_name)
        degree_year = edu_section.find('p',{"class":"pv-entity__dates t-14 t-black--light t-normal"}).find_all('span')[1].get_text().strip()
        edu_details.append(degree_year)
        edu_details1.append(edu_details)
    else:
        edu_details1.append("Detail Not Found!")
        

    #link = browser.find_element_by_link_text('Contact info')   
    #link.click() 
    browser.get ("https://www.linkedin.com" + contact + "detail/contact-info/")
    browser.implicitly_wait(3)
    contact_page = bs(browser.page_source, features="html.parser")
    #print(contact_page)
    name = contact_page.find_all('a',href=re.compile("linkedin.com/in/"))
    content_contact_page = contact_page.find_all('a',href=re.compile("mailto"))
    for contact in content_contact_page:
        #print("[+]", contact.get('href')[7:])
        my_network_emails.append(contact.get('href')[7:])
    for name in name:
        #print(name.get('href'))
        linkedin_link.append(name.get('href'))
    time.sleep(random.uniform(0.5, 1.9))

with open(f'network_emails.csv', 'w') as f:
    writer = csv.writer(f)
    email=0
    while email<len(my_network_emails):
            writer.writerow([name5[email],my_network_emails[email],linkedin_link[email],exp_deatails1[email],edu_details1[email]])
            email+=1



    

