import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import pandas as pandasForSortingCSV
page_limit = True

# setting boolean parameter for page limit
if page_limit == True:
    pages = 100
else:
    pages = 200

#Setting up CSV file
with open('data_scrapy.csv','w') as s: 
    s.write("Name,City,State,Affiliation,Education Level\n")


class careerSpider(scrapy.Spider):

    name = 'myntraSpider'
    allowed_domains = ['myntra.com']
    # start_urls = ["https://school.careers360.com/schools/schools-in-india?page={page}".format(page=page) 
    #               for page in range(1, pages+1)]
    start_urls = ['https://school.careers360.com/schools/schools-in-india']
    for i in range(2,pages+1):
        start_urls.append('https://school.careers360.com/schools/schools-in-india?page=' + str(i))  
    
# Parse the html content
    def parse(self, response):
        schoolName_list = response.xpath('//div[@class="headingBox"]/h3[@class="blockHeading"]/a/text()').getall()
        schoolCity_list = response.xpath('//li[@class="schoolAddress"]/span/a[1]/text()').extract()
        schoolState_list = response.xpath('//li[@class="schoolAddress"]/span/a[2]/text()').extract()
        schoolBoard_list = response.xpath('//li[@class="schoolboardName"]/span/a[1]/text()').extract()
        schoolLevels = response.xpath('//li[@class="schoolGrade"]/span[@class="details"]/text()').extract()
        schoolLevel_list=[]
        # creating a dictionary to store the scraped data in previous step
        for level in schoolLevels:
            schoolLevel_list.append(level.strip())
        data_dictionary = {'Name': schoolName_list, 'City': schoolCity_list, 'State': schoolState_list, 'Affiliation' : schoolBoard_list, 'Education Level':schoolLevel_list }
        
        # storing the scraped data in csv file
        df = pd.DataFrame.from_dict(data_dictionary, orient='index')
        df = df.transpose()
        df.to_csv('data_scrapy.csv', index = False, mode='a',header = False)
            
# run spider
process = CrawlerProcess()
process.crawl(careerSpider)
process.start()
df = pd.read_csv("data_scrapy.csv")
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('data_scrapy.csv', index = False)
