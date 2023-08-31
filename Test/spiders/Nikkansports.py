from w3lib.html import remove_tags
import html
from Test.items import Feed
from  Test.spiders.Central import Central
from Test.settings import logger
import hashlib

class Nikkansports(Central):

    name="nikkansports"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        response.selector.remove_namespaces()
        item    =   Feed()
        for data in response.css("entry"):
            try:
                item['title']   =   html.unescape(data.css('entry>title::text').get())
            except:
                item['title']   =   ''
            link    =   data.xpath("link/@href").get()
            try:
                item['link']    =   link
            except:
                item['link']=''
            result = hashlib.md5(link.encode())
            try:
                item['link_hash']=result.hexdigest()
            except:
                item['link_hash']=''
            try:
                item['description']=html.unescape(remove_tags(data.css('entry>summary::text').get()))
            except:
                item['description']=''
            try:
                item['pubDate']=data.css('entry>published::text').get()
            except:
                item['pubDate']=''
            logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
            
            yield item