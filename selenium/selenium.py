from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import re
import time
import pandas as pd

#setting chrome driver path
path = r"C:\Users\mundhra-1\Desktop\Web Scraping\chromedriver.exe"
ser = Service(path)
driver = webdriver.Chrome(service=ser)

url = 'https://school.careers360.com/schools/schools-in-india'

#calling the website url
driver.get(url)

#maximizing the browser window
driver.maximize_window()

# setting boolean parameter for page limit
page_limit = True

if page_limit == True:
    max_pages = 100
else: max_pages = 200



# declaring lists to store scraped data
schoolName_list = []
schoolCity_list = []
schoolState_list = []
schoolBoard_list=[]
schoolLevel_list=[]



# iterating over first 100 pages to scrap required data
for i in range(1,max_pages+1):
    
    time.sleep(2)
    names = driver.find_elements(By.XPATH,'//div[@class="headingBox"]/h3[@class="blockHeading"]/a')
    for name in range(len(names)):
        schoolName_list.append(names[name].text) 

    time.sleep(2)
    cities = driver.find_elements(By.XPATH,'//li[@class="schoolAddress"]/span/a[1]')
    for city in range(len(cities)):
        schoolCity_list.append(cities[city].text)

    time.sleep(2)
    states = driver.find_elements(By.XPATH,'//li[@class="schoolAddress"]/span/a[2]')
    for state in range(len(states)):
        schoolState_list.append(states[state].text)

    time.sleep(2)
    boards = driver.find_elements(By.XPATH,'//li[@class="schoolboardName"]/span/a[1]')
    for board in range(len(boards)):
        schoolBoard_list.append(boards[board].text)

    time.sleep(2)
    levels = driver.find_elements(By.XPATH,'//li[@class="schoolGrade"]/span[@class="details"]')
    for level in range(len(levels)):
        schoolLevel_list.append(levels[level].text.strip())


     
# using time.sleep for a slight delay in code to interact and find all the elements
    time.sleep(1)
    #driver.implicitly_wait(1)

# pagination xpath to go from first page till 100th page
    driver.find_element(By.CLASS_NAME, value='next').click()
    
    
   
# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Name': schoolName_list, 'City': schoolCity_list, 'State': schoolState_list, 'Affiliation' : schoolBoard_list, 'Education Level':schoolLevel_list }

# storing the scraped data in csv file
#dataframe = pd.DataFrame(data_dictionary)
#dataframe.to_csv('data.csv', mode='a', index=False, header=False, encoding="cp1252")
df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_selenium.csv', index = False)




# closing the driver instance and browser window
driver.quit()

