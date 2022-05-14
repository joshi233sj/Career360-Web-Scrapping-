from bs4 import BeautifulSoup
import requests
from lxml import etree
import time
import pandas as pd


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
for i in range(1, max_pages+1):
    url = 'https://school.careers360.com/schools/schools-in-india?page='+str(i)
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    dom = etree.HTML(str(soup))
    
    names = dom.xpath('//div[@class="headingBox"]/h3[@class="blockHeading"]/a')
    for name in range(len(names)):
        schoolName_list.append(names[name].text) 
    
    cities= dom.xpath('//li[@class="schoolAddress"]/span/a[1]')
    for city in range(len(cities)):
        schoolCity_list.append(cities[city].text)   
        
    states =dom.xpath('//li[@class="schoolAddress"]/span/a[2]')
    for state in range(len(states)):
        schoolState_list.append(states[state].text)
        
    boards=dom.xpath('//li[@class="schoolboardName"]/span/a[1]')
    for board in range(len(boards)):
        schoolBoard_list.append(boards[board].text)
        
    levels=dom.xpath('//li[@class="schoolGrade"]/span[@class="details"]')
    for level in range(len(levels)):
        schoolLevel_list.append(levels[level].text.strip())
   
   
# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Name': schoolName_list, 'City': schoolCity_list, 'State': schoolState_list, 'Affiliation' : schoolBoard_list, 'Education Level':schoolLevel_list }


# storing the scraped data in csv file
#dataframe = pd.DataFrame(data_dictionary)
#dataframe.to_csv('data.csv', mode='a', index=False, header=False, encoding="cp1252")
df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_bsoup.csv',index = False)

