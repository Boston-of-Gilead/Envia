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
# from subprocess import CREATE_NO_WINDOW

chromedriver = "C:\\Users\\USER\\Desktop\\LIFEBOAT\\Desktop\\COMPUTER_STUFF\\SCRIPTS\\chromedriver.exe"

s = Service(chromedriver)
# s.creationflags = CREATE_NO_WINDOW
ua = UserAgent()

chrome_options = webdriver.ChromeOptions() #Make sure chromedriver.exe is in the same directory as the script or this gets ugly)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.add_argument(f'user-agent={ua.random}')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
#Pass webdriver check
#chrome_options.add_argument(f'user-agent={user_agent}')
# chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--start-fullscreen")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--headless") #headless disables the Chrome popup
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--window-size=1420,1080")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 14)
#driver.implicitly_wait(10)

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
    # print(rURL)
    # print(phone)
    # print(mail)
    print(sellerName)
    # print(j)

def outputData():
    #append
    print("Writing data")
    #data = [rURL, phone, mail, sellerName,j]
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerows(data)
        writer.writerow([rURL, phone, mail, sellerName,j])

def scrollPg():
    # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     # Wait to load page
    #     time.sleep(2)
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    #Via SendKeys
    #Too aggressive
    html = driver.find_element(By.TAG_NAME, 'html')
    si = 0
    # while si <= 20:
    #     time.sleep(0.15)
    #     html.send_keys(Keys.PAGE_DOWN) #PAGE_DOWN or END
    #     si = si + 1
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
    #button = wait.until(EC.visibility_of_any_elements_located((By.ID, "sp-cc-rejectall-link"))).click()
    #print("element exists")
except:
    #exit()
    print("Cookie button not found")

#RESULTS PAGE
#As IDs
# pattern =  "\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12}"

# ids = driver.find_elements(By.XPATH,'//*[@id]')
# for ii in ids:
#     returnId = ii.get_attribute('id')    # id name as string
#     #for i in test_list:
#     x = re.findall(pattern, returnId)
#     if x:
#         idList.append(x)
#         #print(x)

# print("Total result ct: ",(len(idList)))

# #
#As role to populate idList
idList = []
# results = driver.find_elements(By.CSS_SELECTOR, "[role]")
# for ii in results:
#     returnRole = ii.get_attribute('role')
#     if returnRole == "listitem":
#         returnId = ii.get_attribute('id')
#         if returnId:
#             idList.append(returnId)
# print("Total result ct:",len(idList))

#Alternative idList method
# cel_widget_id = "MAIN-SEARCH_RESULTS-3" 3 through 69
# OR
# data-image-index = "1" through "60"

#Now we have the ids of the search results in an array
#set primary window
#original_window = driver.current_window_handle

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
        # waiting = wait.until(EC.visibility_of_element_located(By.XPATH, "//img[@data-image-index="f'{j}'"]"))
        # waiting.click()
        print(f"Did not find element {j}, staying on results page: " + driver.current_url) #still on results page
        # print(driver.current_url)
        # exit()
        # driver.close()
        # driver.quit()
        continue
    try:
        print(f"On item page for {j}: " + driver.current_url)
        #triggerName = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")))[1].text
        #triggerName = driver.find_element(By.ID,"sellerProfileTriggerId").text
        trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
        #trigger.click() 
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
            #neither of thes eoptions work here but they don't error out either.
            # driver.back() #back to results page
            #driver.execute_script("window.history.go(-1)") #back to results page
            # Go back with keyboard shortcut
            #print(driver.current_url)
            time.sleep(1)
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ALT + Keys.LEFT_ARROW)
            time.sleep(1)
            #print(driver.current_url)
        except:
            print("Back failed, going manually")
            driver.get(url_str)
        # time.sleep(2.5)
        # print("Headed back to results page")
        # print(driver.current_url)
        continue
exit()

#driver.execute_script("window.history.go(-1)")

##Open them all method - on results page
# j = 0
# print("idlist ct:", len(idList))
# for rId in idList:
#     # print(idList)[j]
#     j = j + 1
#     print("on results pg")
#     if rId:
#         #time.sleep(0.5)
#         print(rId)
#         try:
#             driver.find_element(By.ID, rId).click() #takes you to item page
#             print("rId present, going to item page")
#         except:
#             print("Did not find rId element, staying on results page") #still on results page
#             continue
#         try:
#             #rURL = driver.current_url()
#             print("on item page")
#             trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click() #takes you to DSI page
#             #trigger.click() 
#             print("o/going to DSI page, passed trigger")
#             time.sleep(1)
#             retrieveData()
#             print("data retrieved")
#             time.sleep(1)
#             outputData()
#             print("data should now be output")
#             driver.back() #back to item page
#             print("back to item pg")
#             time.sleep(1)
#             driver.back() #back to results page
#             print("back to results pg")
#         except:
#             print("skipping due to failed trigger, still on item page") #on item page, need to go back to results
#             driver.back() #back to results page
#             print("headed back to results page")
#             continue
#         # try:
#         #     dispatch = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")))[1].text
#         #     print(type(dispatch))
#         #     sdisp = str(dispatch)
#         #     if "Amazon" not in sdisp:
#         #         print("This SHOULD be a non-Amazon")
#         #     print(f"Dispatch info: {sdisp}")
#         # except:
#         #     driver.back()
#         #     continue
#         # print("Got to pre-sort")
#         # time.sleep(0.5)
#         #driver.switch_to.window(original_window)
#         # if "Amazon" in dispatch:
#         #     print("Found an Amazon")
#         #     driver.back()
#         #     continue
#         # else:
#         #     print("Found a non-Amazon")
#         #     rURL = driver.current_url()
#         #     trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click()
#         #     time.sleep(1)
#         #     retrieveData
#         #     time.sleep(1)
#         #     outputData
#         #     driver.back()
#     else:
#         continue
# exit()

# # handles = driver.window_handles
# # print(len(handles))
# # for handle in handles:
# #     if handle != original_window:
# #         driver.switch_to.window(handle)
# #         time.sleep(0.5)
# #         dispatch = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")))[1].text
# #         print(f"Dispatch info: {dispatch}")
# # exit()

# #Older method
# for rId in idList:
#     j = j + 1
#     print(j)
#     #driver.find_element(By.LINK_TEXT, "new window").click()
#     time.sleep(1)
#     if rId:
#         time.sleep(1)
#         driver.find_element(By.ID, rId).click()
#         # dispatch = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")))[1].text
#         # print(f"Dispatch info: {dispatch}")
#         # exit()
#         # lid = len(idList)
#         # print(lid)
#         # handles = driver.window_handles
#         # print(len(handles))
#         #wait.until(EC.number_of_windows_to_be(2))
#         #print(handles)
#         #work on each window
#         for window_handle in driver.window_handles:
#             if window_handle != original_window:
#                 print(window_handle)
#                 driver.switch_to.window(window_handle)
#                 #break
#                 #test for Amazon
#                 #dispatch = driver.find_element(By.CLASS_NAME,'a-size-small offer-display-feature-text-message')
#                 #dispatch = driver.find_element(By.CLASS_NAME,"span.a-size-small.offer-display-feature-text-message")
#                 #dispatch = driver.find_element(By.CLASS_NAME, "'a-size-small offer-display-feature-text-message'")
#                 dispatch = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")))[1].text
#                 #time.sleep(5)
#                 #dispatch = driver.find_element(By.CSS_SELECTOR, "#fulfillerInfoFeature_feature_div span")[1].text
#                 print(f"Dispatch info: {dispatch}")
#                 #print(driver.current_url())
#                 exit()
#                 # dispatch = driver.find_element(By.CSS_SELECTOR,"#fulfillerInfoFeature_feature_div > div.offer-display-feature-text.a-size-small > div.offer-display-feature-text.a-spacing-none.odf-truncation-popover > span")
#                 # look = driver.find_element(By.XPATH,"//span[contains(text(), 'Amazon')]")
#                 # print(look)
#                 # exit()
#                 #dispatch = driver.find_element(By.CSS_SELECTOR,"span.div.offer-display-feature-text.a-spacing-none.odf-truncation-popover")
#                 # time.sleep(30)
#                 # exit()
#                 #//*[@id="merchantInfoFeature_feature_div"]/div[2]/div[1]/span
#                 #dispatch = driver.find_element(By.XPATH,'//*[@id='fulfillerInfoFeature_feature_div']/div[2]/div[1]/span')
#                 #dispatch = driver.find_element(By.XPATH,'//*[@id="merchantInfoFeature_feature_div"]/div[2]/div[1]/span')
#                 #dispatch = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[5]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[21]/div/div/div[1]/div/div[2]/div[2]/div[1]/span")
#                 print("found it")
#                 dispatch = str(dispatch)
#                 print(dispatch)
#                 if "Amazon" in dispatch:
#                     driver.close()
#                     driver.switch_to.window(original_window)
#                     continue
#                 else:
#                     rURL = driver.current_url()
#                     trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click()
#                     time.sleep(1)
#                     retrieveData
#                     time.sleep(1)
#                     outputData
#                     driver.close()
#                     driver.switch_to.window(original_window)
#                     continue

# exit()

# try:
#     rURL = driver.current_url()
#     trigger = driver.find_element(By.ID,"sellerProfileTriggerId").click()
#     time.sleep(1)
#     retrieveData
#     time.sleep(1)
#     outputData
#     driver.back()
# except:
#     driver.back()
#     continue

#Need to search the following attributes as I suspect the IDs are changing
# cel_widget_id = "MAIN-SEARCH_RESULTS-3" 3 through 69
# OR
# data-image-index = "1" through "60"