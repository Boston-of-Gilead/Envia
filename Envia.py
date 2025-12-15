import csv
import os
import re
# import pyautogui
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

chromedriver = "C:\\Users\\USER\\Desktop\\LIFEBOAT\\Desktop\\COMPUTER_STUFF\\SCRIPTS\\chromedriver.exe"

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

def processPg():
    global j
    j = 0
    for j in range(0,76): #76
        #pyautogui.hotkey('f15')
        j = j + 1
        print(f"On results pg {p} " + driver.current_url)
        time.sleep(2)
        scrollPg()
        try:
            driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
            print(f"Going to item page for {j}")
        except:
            #print(driver.current_url)
            print(f"Did not find element {j}, staying on results page: {p} " + driver.current_url) #still on results page
            # if p == 1:
            #     continue
            # else:
            #     input("Press Enter to exit...")
            #     exit()             
        try:
            #print(f"On item page for {j}: " + driver.current_url)
            trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
            #print(f"On/going to DSI page for {j}, passed trigger")
            time.sleep(1)
            retrieveData()
            print(f"Data retrieved for {j}")
            time.sleep(1)
            outputData()
            print(f"Data should now be output for {j}")
            driver.back() #back to item page
            print(f"Back to item pg {j}")
            time.sleep(1)
            driver.back() #back to results page
            print(f"Back to results pg# {p}")
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
    # match p:
    #     case 1:
    #         for j in range(0,61):
    #             j = j + 1
    #             print("On results pg " + driver.current_url)
    #             time.sleep(2)
    #             scrollPg()
    #             try:
    #                 driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
    #                 print(f"Going to item page for {j}")
    #             except:
    #                 print(driver.current_url)
    #                 print(f"Did not find element {j}, staying on results page: {p}" + driver.current_url) #still on results page
    #                 if p == 2:
    #                     input("Press Enter to continue...")
    #                 continue
    #             try:
    #                 print(f"On item page for {j}: " + driver.current_url)
    #                 trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
    #                 print(f"On/going to DSI page for {j}, passed trigger")
    #                 time.sleep(1)
    #                 retrieveData()
    #                 print("Data retrieved")
    #                 time.sleep(1)
    #                 outputData()
    #                 print("Data should now be output")
    #                 driver.back() #back to item page
    #                 print(f"Back to item pg {j}")
    #                 time.sleep(1)
    #                 driver.back() #back to results page
    #                 print("Back to results pg")
    #             except:
    #                 print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
    #                 try:
    #                     time.sleep(1)
    #                     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
    #                     time.sleep(1)
    #                 except:
    #                     print("Back failed, going manually")
    #                     driver.get(url_str)
    #                 continue
    #     case 2:
    #         for j in range(53,98):
    #             j = j + 1
    #             print("On results pg " + driver.current_url)
    #             time.sleep(2)
    #             scrollPg()
    #             try:
    #                 driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
    #                 print(f"Going to item page for {j}")
    #             except:
    #                 print(driver.current_url)
    #                 print(f"Did not find element {j}, staying on results page: {p}" + driver.current_url) #still on results page
    #                 if p == 2:
    #                     input("Press Enter to continue...")
    #                 continue
    #             try:
    #                 print(f"On item page for {j}: " + driver.current_url)
    #                 trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
    #                 print(f"On/going to DSI page for {j}, passed trigger")
    #                 time.sleep(1)
    #                 retrieveData()
    #                 print("Data retrieved")
    #                 time.sleep(1)
    #                 outputData()
    #                 print("Data should now be output")
    #                 driver.back() #back to item page
    #                 print(f"Back to item pg {j}")
    #                 time.sleep(1)
    #                 driver.back() #back to results page
    #                 print("Back to results pg")
    #             except:
    #                 print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
    #                 try:
    #                     time.sleep(1)
    #                     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
    #                     time.sleep(1)
    #                 except:
    #                     print("Back failed, going manually")
    #                     driver.get(url_str)
    #                 continue
    #     case 3:
    #         for j in range(101,146):
    #             j = j + 1
    #             print("On results pg " + driver.current_url)
    #             time.sleep(2)
    #             scrollPg()
    #             try:
    #                 driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
    #                 print(f"Going to item page for {j}")
    #             except:
    #                 print(driver.current_url)
    #                 print(f"Did not find element {j}, staying on results page: {p}" + driver.current_url) #still on results page
    #                 if p == 2:
    #                     input("Press Enter to continue...")
    #                 continue
    #             try:
    #                 print(f"On item page for {j}: " + driver.current_url)
    #                 trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
    #                 print(f"On/going to DSI page for {j}, passed trigger")
    #                 time.sleep(1)
    #                 retrieveData()
    #                 print("Data retrieved")
    #                 time.sleep(1)
    #                 outputData()
    #                 print("Data should now be output")
    #                 driver.back() #back to item page
    #                 print(f"Back to item pg {j}")
    #                 time.sleep(1)
    #                 driver.back() #back to results page
    #                 print("Back to results pg")
    #             except:
    #                 print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
    #                 try:
    #                     time.sleep(1)
    #                     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
    #                     time.sleep(1)
    #                 except:
    #                     print("Back failed, going manually")
    #                     driver.get(url_str)
    #                 continue
    #     case 4:
    #         for j in range(149,194):
    #             j = j + 1
    #             print("On results pg " + driver.current_url)
    #             time.sleep(2)
    #             scrollPg()
    #             try:
    #                 driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
    #                 print(f"Going to item page for {j}")
    #             except:
    #                 print(driver.current_url)
    #                 print(f"Did not find element {j}, staying on results page: {p}" + driver.current_url) #still on results page
    #                 if p == 2:
    #                     input("Press Enter to continue...")
    #                 continue
    #             try:
    #                 print(f"On item page for {j}: " + driver.current_url)
    #                 trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
    #                 print(f"On/going to DSI page for {j}, passed trigger")
    #                 time.sleep(1)
    #                 retrieveData()
    #                 print("Data retrieved")
    #                 time.sleep(1)
    #                 outputData()
    #                 print("Data should now be output")
    #                 driver.back() #back to item page
    #                 print(f"Back to item pg {j}")
    #                 time.sleep(1)
    #                 driver.back() #back to results page
    #                 print("Back to results pg")
    #             except:
    #                 print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
    #                 try:
    #                     time.sleep(1)
    #                     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
    #                     time.sleep(1)
    #                 except:
    #                     print("Back failed, going manually")
    #                     driver.get(url_str)
    #                 continue
    #     case 5:
    #         for j in range(197,242):
    #             j = j + 1
    #             print("On results pg " + driver.current_url)
    #             time.sleep(2)
    #             scrollPg()
    #             try:
    #                 driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
    #                 print(f"Going to item page for {j}")
    #             except:
    #                 print(driver.current_url)
    #                 print(f"Did not find element {j}, staying on results page: {p} " + driver.current_url) #still on results page
    #                 if p == 2:
    #                     input("Press Enter to continue...")
    #                 continue
    #             try:
    #                 print(f"On item page for {j}: " + driver.current_url)
    #                 trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
    #                 print(f"On/going to DSI page for {j}, passed trigger")
    #                 time.sleep(1)
    #                 retrieveData()
    #                 print("Data retrieved")
    #                 time.sleep(1)
    #                 outputData()
    #                 print("Data should now be output")
    #                 driver.back() #back to item page
    #                 print(f"Back to item pg {j}")
    #                 time.sleep(1)
    #                 driver.back() #back to results page
    #                 print("Back to results pg")
    #             except:
    #                 print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
    #                 try:
    #                     time.sleep(1)
    #                     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
    #                     time.sleep(1)
    #                 except:
    #                     print("Back failed, going manually")
    #                     driver.get(url_str)
    #                 continue
        # case 6:
        #     exit()

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
        writer.writerow([rURL, phone, mail, sellerName, j, p])

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
data = [['URL', 'Phone', 'Email', 'Dispatcher','Index','Page']]
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

p = 1
#RESULTS PAGE
#Data image index method - on results page
processPg()
# for j in range(0,61):
#     j = j + 1
#     print("On results pg " + driver.current_url)
#     time.sleep(2)
#     scrollPg()
#     try:
#         driver.find_element(By.XPATH, "//img[@data-image-index="f'{j}'"]").click() #takes you to item page
#         print(f"Going to item page for {j}")
#     except:
#         print(driver.current_url)
#         print(f"Did not find element {j}, staying on results page: " + driver.current_url) #still on results page
#         continue
#     try:
#         print(f"On item page for {j}: " + driver.current_url)
#         trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
#         print(f"On/going to DSI page for {j}, passed trigger")
#         time.sleep(1)
#         retrieveData()
#         print("Data retrieved")
#         time.sleep(1)
#         outputData()
#         print("Data should now be output")
#         driver.back() #back to item page
#         print(f"Back to item pg {j}")
#         time.sleep(1)
#         driver.back() #back to results page
#         print("Back to results pg")
#     except:
#         print(f"Skipping due to failed trigger (meaning Dispatched by Amazon), still on item page for {j}: " + driver.current_url) #on item page, need to go back to results
#         try:
#             time.sleep(1)
#             driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
#             time.sleep(1)
#         except:
#             print("Back failed, going manually")
#             driver.get(url_str)
#         continue
#exit()

#https://www.amazon.es/-/en/s?k=botas&page=2&xpid=z54Yzi6Xb7aFI&crid=3FAMIX7GV5DUR&qid=1765472496&sprefix=bot%2Caps%2C747&ref=sr_pg_2

#https://www.amazon.es/-/en/s?k=botas&page=2

#/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[69]/div/div/span/ul/li[3]/span/a
#li.s-list-item-margin-right-adjustment:nth-child(4) > span:nth-child(1) > a:nth-child(1)
#li.s-list-item-margin-right-adjustment:nth-child(3) > span:nth-child(1) > a:nth-child(1)

print("LOOP")

for p in range(1,5):
    p = p + 1
    #https://www.amazon.es/s?k=botas&page=3&language=es
    newUrl = f"https://www.amazon.es/-/es/s?k={search}&page={p}"
    print(f"Going to next page {p} at {newUrl}")
    driver.get(newUrl)
    time.sleep(2)
    processPg()
    # input("Press Enter to continue...")
    # continue
