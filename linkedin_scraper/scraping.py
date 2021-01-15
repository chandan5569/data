from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection
import random
import sys

def linkedin_scraper():
    # Email_id = input("Please enter the login email: ")
    # Password = input("Please enter the password: ")
    # start_page_number = int(input("From which page to start: "))
    # end_page_number = int(input("At which page to end: "))
    User_id = sys.argv[1]
    Email_id = sys.argv[2]
    Password = sys.argv[3]
    start_page_number = int(sys.argv[4])
    end_page_number = int(sys.argv[5])


    
    client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.linkedinContacts
    
    # print(Email_id)
    # print(Password)
    # print(start_page_number)
    # print(end_page_number)
    sleeps = [2, 3, 4, 5, 6, ]
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')

    # PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
    # driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    PATH = r"/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver.get("https://www.linkedin.com/login")

    driver.find_element_by_id("username").send_keys(Email_id)
    time.sleep(5)
    password = driver.find_element_by_id("password")
    password.send_keys(Password)
    time.sleep(random.choice(sleeps))

    password.send_keys(Keys.RETURN)
    time.sleep(5)
    
    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
        print("Incorrect login details")
        linkedin_scraper()

    if 'https://www.linkedin.com/checkpoint/lg/login?errorKey=challenge_global_internal_error' in driver.current_url:
        print("Sorry something went wrong. Please try again later")
        linkedin_scraper()

    def otp():
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

    if 'https://www.linkedin.com/checkpoint' in driver.current_url:
        otp()

    if driver.current_url == 'https://www.linkedin.com/checkpoint/challenge/verify':
        print("Incorrect OTP")
        otp()
    
    data = []
    data_csv = []
    my_db.linkedin_otp.drop()
    
    print("Scraping in progress")
    my_db.linkedin_otp.drop()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    time.sleep(5)
    prof = soup.find("aside", {"class": "left-rail"})
    prof = prof.find('a')['href']
    profile_link = f"https://www.linkedin.com{prof}"

    driver.get(profile_link)
    #     print(driver.current_url)
    time.sleep(2)
    soup1 = BeautifulSoup(driver.page_source, features="html.parser")
    time.sleep(4)
    connection_page = soup1.find("a", attrs={"data-control-name": "topcard_view_all_connections"})['href']
    connection_page = f"https://www.linkedin.com/{connection_page}"

    driver.get(connection_page)
    #     print(driver.current_url)

    while start_page_number <= end_page_number:

        url = f"{connection_page}&page={start_page_number}"
        driver.get(url)
        time.sleep(random.choice(sleeps))
        #         print(driver.current_url)
        length = driver.execute_script("return document.documentElement.scrollHeight")
        for i in range(100, length, 100):
            driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, features="html.parser")
        time.sleep(random.choice(sleeps))
        time.sleep(3)
        container = soup.find("div", attrs={"role": "main"})
        container = container.find("ul")
        #         if container is None:
        #             break
        profiles = container.find_all("li")
        # for i in profiles:
        #     print(i.find('a')['href'])
        #         print("Going to connection list")
        for profile in profiles:
            #             print("Entered profile")
            profile = profile.find('a')['href']
            if "https://www.linkedin.com" not in profile:
                profile = f"https://www.linkedin.com{profile}"
            #             print(profile)
            driver.get(profile)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            time.sleep(random.choice(sleeps))
            link = f"{driver.current_url}detail/contact-info"
            #             print(link)
            driver.get(link)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            time.sleep(random.choice(sleeps))

            sites = []
            phone = ''
            email = ''
            ims = []
            address = ''
            detail = []
            extra_links = []

            names = soup.find("div", {"class": "artdeco-modal__header ember-view"})
            name = names.find("h1").text.strip()
            #             print(name)

            container = soup.find("div", attrs={"class": "pv-profile-section__section-info section-info"})
            sections = container.find_all("section")
            for section in sections:
                text = section.find('header').text.strip()
                #                 print(text)
                if "Profile" in text:
                    linkedin_url = section.find('a')['href']
                    #                     print(linkedin_url)
                    continue
                if "Website" in text:
                    websites = section.find_all('li')

                    for website in websites:
                        #                         print(website.find('a')['href'])
                        sites.append(website.find('a')['href'])
                    continue
                if text == "Phone":
                    phone = section.find("span").text
                    #                     print(phone)
                    continue
                if text == 'Address':
                    address = section.find('a')['href']
                    address = address.split('=')[1:]
                    address = ' '.join(address)
                    address = address.strip()
                    #                     print(address)
                    continue
                if text == 'Email':
                    email = section.find('a')['href']
                    email = email.split(':')[1:]
                    email = ''.join(email)
                    email = email.strip()
                    #                     print(email)
                    continue
                if text == "IM":
                    im = section.find_all("li")
                    for i in im:
                        spans = i.find_all("span")

                        for span in spans:
                            detail.append(span.text.strip())
                        ims = '-'.join(detail)
#                         print(ims)
                    continue
                if "Connected" in text:
                    continue
                extra_link = section.find('a')
                if extra_link is not None:
                    extra_link = extra_link['href']
#                     print(extra_link)
                    extra_links.append(extra_link)

            if len(sites) == 0:
                sites = ''
            if len(ims) == 0:
                ims = ''
            if extra_links == 0:
                extra_links = ''
            driver.get(profile)
            time.sleep(5)
            time.sleep(random.choice(sleeps))

            length = driver.execute_script("return document.documentElement.scrollHeight")
            length
            for i in range(100, length, 200):
                driver.execute_script("window.scrollTo(0, " + str(i) + ")")
                time.sleep(2)

            soup = BeautifulSoup(driver.page_source, features="html.parser")
            time.sleep(random.choice(sleeps))
            exp = soup.find('section', attrs={"id": "experience-section"})

            if exp != None:
                exp = exp.find('ul').find_all('li')
                experience = []
                for ex in exp:
                    designation = ex.find('h3')
                    if designation == -1:
                        continue
                    if designation == None:
                        designation = ''
                    else:
                        designation = designation.text.strip()

                    company = ex.find('p', {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
                    if company == -1:
                        continue
                    company = ex.find('p', {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
                    if company == None:
                        company = ''
                    else:
                        company = company.text.strip()
                    if 'time' in company:
                        company = company.split()[:-1]
                        company = ' '.join(company)
                    if '\n' in company:
                        company = company.replace('\n', '')
                        company = company.split()[0]

                    duration = ex.find('h4')
                    if duration == None:
                        duration = ''
                    else:
                        duration = duration.text.strip()
                        duration = duration.split(' ')[2:]
                        duration = ''.join(duration)

#                     print(designation)
#                     print(company)
#                     print(duration)
                    experience.append({"Company": company, "Designation": designation, "Duration": duration})
            else:
                experience = "No details found"
            #             print(experience)
            time.sleep(random.choice(sleeps))
            schoolings = soup.find("section", attrs={"id": "education-section"})
            if schoolings != None:
                schooling = schoolings.find('ul').find_all('li')
                schools = []
                for i in schooling:
                    if i.find('h3') == None:
                        continue
                    school = i.find('h3').text.strip()
                    schools.append({"School": school})
            else:
                schools = "Education details not found"

            # print({"Name": name, "Experience": experience, "Education": schools, "LinkedIn URL": linkedin_url,"Websites": sites, "Phone": phone, "Address": address, "Email": email, "Instant Messenger": ims, "Links": extra_links})
            # db.insert({"Name": name, "Experience": experience, "Education": schools, "LinkedIn URL": linkedin_url, "Websites": sites, "Phone": phone, "Address": address, "Email": email, "Instant Messenger": ims, "Links": extra_links})
            data.append({"Name": name, "Experience": experience, "Education": schools, "LinkedIn_URL": linkedin_url, "Websites": sites, "Phone": phone, "Address": address, "Email": email, "Instant_Messenger": ims, "Links": extra_links})


            time.sleep(10)
            # print("PROFILE SCRAPED")
        start_page_number += 1

    # print("You exceeded the page limit")
    print("Scraping stopped")
    db.insert({"User_Id": User_id, "linkedin_login_email": Email_id, "collectionOfContacts": data})
    dataset = pd.DataFrame(data, columns=['User_id','linkedin_login_email','Name', 'Experience', 'Education', 'LinkedIn_URL', 'Websites', 'Phone', 'Address', 'Email', 'Instant_Messenger', 'Links'])
    dataset.to_csv('details.csv')

    # data_csv.append({"User_id": "user_id", "linkedin_login_email": Email_id, "collectionOfContacts": data})
    # dataset1 = pd.DataFrame(data_csv, columns=['User_id', 'linkedin_login_email','collectionOfContacts'])
    # dataset1.to_csv('details1.csv')

linkedin_scraper()