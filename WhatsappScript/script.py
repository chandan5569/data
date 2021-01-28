from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time


options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver.get('https://web.whatsapp.com/')
print("Scan QR Code in the browser and then press Enter")
input()



owner_num = input("Enter the number of the owner of the group\n")
member_nums = input("Enter the number of members seperated by comma\n")
member_nums = member_nums.split(',')
group_name = input('Enter the group name\n')
message = input('Enter the message to be posted in the group\n')
if owner_num not in member_nums:
    member_nums.append(owner_num)


try:

    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="side"]/header/div/div/span/div/div[@title="Menu"]'))

    )
    menu.click()


    new_group = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="New group"]'))
    )
    new_group.click()


    input_members = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Type contact name"]'))
    )
    for i in member_nums:
        try:
            input_members.send_keys(i)
            input_members.send_keys(Keys.RETURN)
        except:
            print('Error with number', i)
    
    confirm_members = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span/div[contains(@class, "copyable-area")]/div/span/div[@role="button"]'))

    )
    confirm_members.click()

    group_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
    )
    group_name_input.send_keys(group_name)

    

    confirm_group_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span/div/div[@tabindex="0"]'))
    )
    confirm_group_name.click()

    message_group = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//footer[@tabindex="-1"]/div/div[@tabindex="-1"]/div[@tabindex="-1"]/div[@contenteditable="true"]'))
    )
    message_group.send_keys(message)
    message_group.send_keys(Keys.RETURN)


    group_info_dots = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="main"]/header/div/div/div/div[@title="Menu"]'))
    )
    group_info_dots.click()

    group_info_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Group info"]'))
    )
    group_info_menu.click()


    group_settings = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Group Settings"]'))
    )
    group_settings.click()


    edit_group_admins = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Edit group admins"]'))
    )
    edit_group_admins.click()


    group_admin_inp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "copyable-area")]/div[@tabindex="-1"]/div/label/div/div[@contenteditable="true"]'))
    )
    group_admin_inp.send_keys(owner_num)
    group_admin_inp.send_keys(Keys.RETURN)

    finalize_admin = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div/div/span/div/div[@data-animate-btn="true"]/div[@role="button"]'))
    )
    finalize_admin.click()
    
    print("Group creation successful")
except:
    driver.quit()


try:
    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="side"]/header/div/div/span/div/div[@title="Menu"]'))

    )
    menu.click()

    new_group = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Log out"]'))
    )
    new_group.click()
except: 
    pass

driver.quit()