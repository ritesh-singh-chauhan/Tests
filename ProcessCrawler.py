from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Test.settings import logger

class ProcessCrawler:

    def __init__(self):
        self.process =  CrawlerProcess(get_project_settings())
        
    def feeds(self,spidername,sourcelink):
        self.process.crawl(spidername,sourcelink)
        self.process.start()
    
    def feed_fd(self,spider_fd,url):

        try:
            self.process.crawl(spider_fd,url)
            self.process.start()

        except Exception as error:
            logger.error(f"Error found in full description from ProcessCrawler:{error}")