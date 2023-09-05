import scrapy
from pandas import read_csv
from Test.items import AutomateItem
import csv

class Automate(scrapy.Spider):

    url=[]
    name='automate'

    filename = '/home/ritesh/projects/testprojects/ScrapyLocalHost/collect_data_sheet.csv'
    with open(filename, 'r',  encoding='ISO-8859-1') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            url.append(row[1])
    
    def start_requests(self):
        print(self.url)
        for url in self.url:
            yield scrapy.Request(url=url, callback=self.parse,
                           headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
                           )
            
    def parse(self,response):
        response.selector.remove_namespaces()
        print("Hello...   ....  .....  ....  ...")
        print("Hello...   ....  .....  ....  ...")

        item           =   AutomateItem()
        
        item['domain']      =   response.url
        item['title']       =   response.xpath("//title/text()").get()
        item['description'] =   response.xpath('//meta[@name="description"]/@content').get()
        print(item,"sdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd1")
        yield item