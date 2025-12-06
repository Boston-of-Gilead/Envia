import csv
import os
import re
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#chromedriver = "C:\\Users\\USER\\Desktop\\LIFEBOAT\\Desktop\\COMPUTER_STUFF\\SCRIPTS\\chromedriver.exe"
chromedriver = "C:\\Users\\Envia\\Documents\\chromedriver.exe"

s = Service(chromedriver)
ua = UserAgent()

chrome_options = webdriver.ChromeOptions() #Make sure chromedriver.exe is in the same directory as the script or this gets ugly)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.add_argument(f'user-agent={ua.random}')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 14)

def retrieveData():
    global rURL
    global phone
    global mail
    global sellerName
    try:
        rURL = driver.current_url
        print(rURL)
    except:
        print("failed to print URL")
    phone = (driver.find_element(By.CSS_SELECTOR,"#page-section-detail-seller-info > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > span:nth-child(2)")).text
    mail = (driver.find_element(By.CSS_SELECTOR,"#page-section-detail-seller-info > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > span:nth-child(2)")).text
    sellerName = (driver.find_element(By.CSS_SELECTOR,"#seller-name")).text

def outputData():
    #append
    print("Writing data")
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([rURL, phone, mail, sellerName,j])

def scrollPg():
    #Via SendKeys
    html = driver.find_element(By.TAG_NAME, 'html')
    si = 0
    while si <= 5:
        time.sleep(0.2)
        html.send_keys(Keys.PAGE_DOWN) #PAGE_DOWN or END
        si = si + 1

#####
#####
#search = input("Termino de busqueda:")
search = "botas"
#####
#####

#initialize output
filename = 'Envia-' + search + '.csv'
data = [['URL', 'Phone', 'Email', 'Dispatcher','Index']]
#with open('Envia.csv', 'w', newline='') as csvfile:
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

#form URL
url_base = "https://www.amazon.es/s?k="
url_str = url_base + search

#Go to Amazon
driver.get(url_str)
time.sleep(1)

#decline cookies
try:
    time.sleep(2)
    button = driver.find_element(By.ID, "sp-cc-rejectall-link").click()
except:
    print("Cookie button not found")

#RESULTS PAGE
#Data image index method - on results page
for j in range(0,61):
    j = j + 1
    print("On results pg " + driver.current_url)
    time.sleep(2)
    scrollPg()
    try:
        driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
        print(f"Going to item page for {j}")
    except:
        print(driver.current_url)
        print(f"Did not find element {j}, staying on results page: " + driver.current_url) #still on results page
        continue
    try:
        print(f"On item page for {j}: " + driver.current_url)
        trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
        print(f"On/going to DSI page for {j}, passed trigger")
        time.sleep(1)
        retrieveData()
        print("Data retrieved")
        time.sleep(1)
        outputData()
        print("Data should now be output")
        driver.back() #back to item page
        print(f"Back to item pg {j}")
        time.sleep(1)
        driver.back() #back to results page
        print("Back to results pg")
    except:
        print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
        try:
            time.sleep(1)
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
            time.sleep(1)
        except:
            print("Back failed, going manually")
            driver.get(url_str)
        continue
exit()




