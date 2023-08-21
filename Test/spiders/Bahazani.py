import html
import hashlib
from w3lib.html import remove_tags
from Test.spiders.Central import Central
from Test.items import TestItem
from Test.settings import logger

class Bahazani(Central):

    name="bahazani"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item=TestItem()
        response.selector.remove_namespaces()
        for data in response.xpath("//item"):
            try:
                item['title']=data.xpath("title/text()").get()
            except:
                item['title']=''
            try:
                link=data.xpath("link/text()").get()
                item['link']=link
            except:
                item['link']=''
            try:
                result=hashlib.md5(link.encode())
                item['link_hash']=result.hexdigest()
            except:
                item['link_hash']=''
            try:
                item['description']=html.unescape(remove_tags(data.xpath("description/text()").get()))
            except:
                item['description']=''
            try:
                item['pubDate']=data.xpath("pubDate/text()").get()
            except:
                item['pubDate']=''
            logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
            
            yield item