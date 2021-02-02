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





def send_connection_request():

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


    def scroll():
        length = driver.execute_script("return document.documentElement.scrollHeight")
        for i in range(100, length, 200):
                driver.execute_script("window.scrollTo(0, " + str(i) + ")")
                time.sleep(2)
###########################################################################################################    
    def chatWindow():
        try:
            chatOpen = driver.find_element_by_xpath("//*[@id='msg-overlay']/div[1]/div")
            # personal_chatOpen = driver.find_element_by_xpath("//div[@id='overlay.close_conversation_window']")

            if chatOpen:
                chatClose = driver.find_element_by_xpath("(//*[@id='msg-overlay']/div[1]/header/section[1])")
                chatClose.click()
                print("Chatbox Closed...")
                return True
            # if personal_chatOpen:
            #     close_personal_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
            #     close_personal_chat.click()
            #     print("Chat closed")
            #     return True
                
        except:
            print("Chatbox is already closed")
            return True
        
###########################################################################################################    
    
    def get_contact_info():
        sites = []
        phone = ''
        email = ''
        ims = []
        detail = []
        extra_links = []
        #getting to contact-info page
        driver.get(link)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        time.sleep(random.choice(sleeps))

        #getting name
        names = soup.find("div", {"class": "artdeco-modal__header ember-view"})
        name = names.find("h1").text.strip()

        #contact sections
        container = soup.find("div", attrs={"class": "pv-profile-section__section-info section-info"})
        sections = container.find_all("section")

        for section in sections:
                    text = section.find('header').text.strip()
                    print(text)
                    if "Profile" in text:
                        linkedin_url = section.find('a')['href']
                        print(linkedin_url)
                        continue
                    if "Website" in text:
                        websites = section.find_all('li')

                        for website in websites:
                            print(website.find('a')['href'])
                            sites.append(website.find('a')['href'])
                        continue
                    if text == "Phone":
                        phone = section.find("span").text
                        print(phone)
                        continue
                    if text == 'Email':
                        email = section.find('a')['href']
                        email = email.split(':')[1:]
                        email = ''.join(email)
                        email = email.strip()
                        print(email)
                        continue
                    if text == "IM":
                        im = section.find_all("li")
                        for i in im:
                            spans = i.find_all("span")

                            for span in spans:
                                detail.append(span.text.strip())
                            ims = '-'.join(detail)
                        continue
                    if "Connected" in text:
                        continue
                    extra_link = section.find('a')
                    if extra_link is not None:
                        extra_link = extra_link['href']
                        extra_links.append(extra_link)

        if len(sites) == 0:
            sites = ''
        if len(ims) == 0:
            ims = ''
        if extra_links == 0:
            extra_links = ''
        # driver.get(link)

        return name, linkedin_url, email, phone, sites, ims, extra_links
###########################################################################################################    
    def get_experience_info():
        time.sleep(random.choice(sleeps))
        driver.get(profile_link)
        length = driver.execute_script("return document.documentElement.scrollHeight")
        for i in range(100, length, 200):
            driver.execute_script("window.scrollTo(0, " + str(i) + ")")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, features="html.parser")
        time.sleep(random.choice(sleeps))
        exp = soup.find('section', attrs={"id": "experience-section"})
        if exp != None:
            exp = exp.find('ul').find_all('li')
            exp1_len = len(exp)
            experience = []
            for enu,ex in enumerate(exp):
                exp_check = ex.find('ul')
                exp_len=10
                if enu < 1:
                    if exp_check is not None:
                        exp_check = exp_check.find_all('li')
                        exp_len = len(exp_check)
                        for e in exp_check:
                            designation = e.find('h3')
                            if designation == -1:
                                continue
                            if designation == None:
                                designation = ''
                            else:
                                designation = designation.text.strip()
                                designation = designation.replace('\n', ' ')
                                designation = designation.split(' ')[1:]
                                designation = ' '.join(designation)
    #                             print(designation)

                            company = ex.find('h3').text.strip()
                            company = company.replace('\n', ' ')
                            company = company.split(' ')[2:]
                            company = ' '.join(company)
    #                         print(company)

                            durations = e.find_all('h4')
                            duration = durations[1].text.strip()
                            duration = duration.replace('\n', ' ')
                            duration = duration.split(' ')[2:]
                            duration = ' '.join(duration)
    #                         print(duration)
                            experience.append({"Company": company, "Designation": designation, "Duration": duration})



                    else:
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
                            experience.append({"Company": company, "Designation": designation, "Duration": duration})
                        if enu+1 == exp_len:
                            break
                try:
                    designation = exp[exp_len+1].find('h3')
                    if designation == -1:
                        continue
                    if designation == None:
                        designation = ''
                    else:
                        designation = designation.text.strip()

                    company = exp[exp_len+1].find('p', {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
                    if company == -1:
                        continue
                    company = exp[exp_len+1].find('p', {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
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

                    duration = exp[exp_len+1].find('h4')
                    if duration == None:
                        duration = ''
                    else:
                        duration = duration.text.strip()
                        duration = duration.replace('\n', ' ')
                        duration = duration.split(' ')[2:]
                        duration = ''.join(duration)

                    experience.append({"Company": company, "Designation": designation, "Duration": duration})
                except Exception as e:
    #                 print(e)
                    print("Done")



        else:
            experience = "No details found"

        return experience
###########################################################################################################    
    def get_education_info():
        soup = BeautifulSoup(driver.page_source, 'html.parser')
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
        return schools
    
    
###########################################################################################################    
    
    User_id = sys.argv[1]
    Email_id = sys.argv[2]
    Password = sys.argv[3]
    keyword = sys.argv[4]
    location = sys.argv[5]
    message = sys.argv[6]
    limit = int(sys.argv[7])
    sleeps = [2,3,4]
    print(Email_id)
    print(Password)
    print(keyword)
    print(location)
    print(message)
    print(limit)
    
    client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
    my_db = client['dreamjobpal']
    db = my_db.linkedinContacts
    
    PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    
    sleeps = [2,3,4]
    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_id("username").send_keys(Email_id)
    password = driver.find_element_by_id("password")
    time.sleep(random.choice(sleeps))
    password.send_keys(Password)
    password.send_keys(Keys.RETURN)
    
    if 'https://www.linkedin.com/checkpoint' in driver.current_url:
        otp()
    print('Login...')
    
    my_db.linkedin_otp.drop()

    time.sleep(4)
    chatWindow()
    search = driver.find_element_by_class_name("search-global-typeahead__input ")
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    print("Entered keyword")
    time.sleep(10)
    
    people = driver.find_element_by_xpath("//button[@aria-label='People']")
    people.click()
    time.sleep(random.choice(sleeps))
    #selecting location(India)
    time.sleep(5)
    container = driver.find_element_by_xpath("//button[@aria-label='Locations filter. Clicking this button displays all Locations filter options.']")
    container.click()
    time.sleep(random.choice(sleeps))
    chatWindow()
    enter_location = driver.find_element_by_xpath("//input[@placeholder='Add a location']")
    # enter_location
    enter_location.send_keys(location)
    time.sleep(5)

    find_location = driver.find_element_by_xpath("//div[@role='listbox']")
    print(find_location)
    select_location = find_location.find_element_by_xpath("//div[@role='option']")
    select_location.click()

    select_location = driver.find_elements_by_xpath("//div[@class='artdeco-hoverable-content__shell']//button[@aria-label='Apply selected filter and show results']")
    select_location[1].click()
    time.sleep(random.choice(sleeps))
    url = driver.current_url
    pagination = url
    print(pagination)
    pagination
    count = 1
    page = 1
    data = []
    while count <= limit:
    
        pagination = f"{pagination}&page={page}"
        print("Pagination", pagination)
        driver.get(pagination)
        chatWindow()
        length = driver.execute_script("return document.documentElement.scrollHeight")
        scroll()
        driver.execute_script("window.scrollTo("+str(length)+",0)")
        i = 125
        result_list = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        container = soup.find("div", attrs={"role": "main"})
        profiles = container.find_all("li")    

        for enu,result in enumerate(result_list):
                time.sleep(5)
                chatWindow()
                if count <= limit:
                    try:
                        #Click on onnect button
                        connect = result.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
                        print("Clicking on Connect")
                        time.sleep(5)

                        connect.click()
                        #ActionChains(driver).click(connect).perform()
                        time.sleep(random.choice(sleeps))
                        print("Sending request...")

                        #adding Note
                        add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                        add_note.click()
                        time.sleep(random.choice(sleeps))
                        add_note = driver.find_element_by_xpath("//textarea[@name='message']")
                        add_note.send_keys(message)
                        time.sleep(random.choice(sleeps))

                        #sending note
                        send_req = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                        send_req.click()
                        print("Request Sent")
                        time.sleep(random.choice(sleeps))
                        count +=1 
                        time.sleep(random.choice(sleeps))
                        profile_link = profiles[enu].find('a')['href']
                        driver.get(profile_link)
                        link = f"{driver.current_url}detail/contact-info"
#                         link
                        name, linkedin_url, email, phone, sites, ims, extra_links = get_contact_info()
                        time.sleep(random.choice(sleeps))

                        experience = get_experience_info()
                        time.sleep(random.choice(sleeps))

                        schools = get_education_info()
                        time.sleep(random.choice(sleeps))
                        data.append({"Name": name, "Experience": experience, "Education": schools, "LinkedIn_URL": linkedin_url, "Websites": sites, "Phone": phone, "Email": email, "Instant_Messenger": ims, "Links": extra_links, "Invitation_Status": "Pending" })
                        driver.get(pagination)
                    except:
                        print("Connection request not sent this user")
    #                     traceback.print_exc()
                else:
                    break
                driver.execute_script("window.scrollTo(0, " + str(i) + ")")
                if i + 125 < length: #increasing for scroll length
                    i += 125
            # print(page)
        page +=1
    print("All requests sent")
    req_data = []
    req_data.append({"linkedin_login_email": Email_id, "Keyword": keyword, "Location": location, "Message/Note": message, "Number_of_requests_Sent": limit, "Request_sent_to": data})
    db.insert({"User_Id": User_id, "Invitation_Details": req_data })


send_connection_request()
