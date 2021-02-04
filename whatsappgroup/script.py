# bnk
import unittest
import HtmlTestRunner
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_PATH

class ViewGroupDetails(unittest.TestCase):
    # declare variable to store the URL to be visited
    base_url="https://web.whatsapp.com/"
    owner_num = input("Enter the number of the owner of the group\n")
    member_nums = input("Enter the number of members separated by comma\n")
    member_nums = member_nums.split(',')
    group_name = input('Enter the group name\n')
    message = input('Enter the message to be posted in the group\n')
    if owner_num not in member_nums:
        member_nums.append(owner_num)

    

    # --- Pre - Condition ---
    def setUp(self):
        # declare and initialize driver variable
        options = webdriver.ChromeOptions()
        options.add_argument(CHROME_PROFILE_PATH)
        self.driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",options=options)       
        # browser should be loaded in maximized window
        self.driver.maximize_window()
         # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.implicitly_wait(10)  #10 is in seconds

    # --- Steps for Whatsapp_Group_TC_001 ---
    def test_WhatsApp_Group_TC_001_create_group(self):
        """User should be able to load WhatsApp Web’s Home Page"""
        # to initialize a variable to hold reference of webdriver instance being passed to the function as a reference.
        driver=self.driver
        # to load a given URL in browser window
        self.driver.get(self.base_url)
        
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'landing-window')))

        self.driver.find_element_by_xpath('//div[@id="side"]/header/div/div/span/div/div[@title="Menu"]').click()
    
        self.driver.find_element_by_xpath('//div[@title="New group"]').click()

        searchTextBox=self.driver.find_element_by_xpath('//input[@placeholder="Type contact name"]')
        for i in self.member_nums:
            searchTextBox.send_keys(i)
            searchTextBox.send_keys(Keys.RETURN)
            searchTextBox.clear()
        self.driver.find_element_by_xpath('//span/div[contains(@class, "copyable-area")]/div/span/div[@role="button"]').click()

        group_name_inp=self.driver.find_element_by_xpath('//div[@contenteditable="true"]')
        group_name_inp.send_keys(self.message)
        self.driver.find_element_by_xpath('//span/div/div[@tabindex="0"]').click()
        
        message_send=self.driver.find_element_by_xpath('//footer[@tabindex="-1"]/div/div[@tabindex="-1"]/div[@tabindex="-1"]/div[@contenteditable="true"]')
        message_send.send_keys(self.message)
        message_send.send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath('//div[@id="main"]/header/div/div/div/div[@title="Menu"]').click()
        
        self.driver.find_element_by_xpath('//div[@title="Group info"]').click()


        self.driver.find_element_by_xpath('//span[text()="Group Settings"]').click()


        self.driver.find_element_by_xpath('//span[text()="Edit group admins"]').click()


        group_admin_inp = self.driver.find_element_by_xpath('//div[contains(@class, "copyable-area")]/div[@tabindex="-1"]/div/label/div/div[@contenteditable="true"]')
        group_admin_inp.send_keys(self.owner_num)
        group_admin_inp.send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath('//div/div/span/div/div[@data-animate-btn="true"]/div[@role="button"]').click()
        self.assertTrue(int((self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').text)==self.message))
    
     # --- post - condition ---
    def tearDown(self):
        # to close the browser
        self.driver.quit()
        
if __name__ == '__main__':
    print("Scan the QR code in the browser")
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:\\Users\\Nishith\\Downloads'))