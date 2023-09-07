from w3lib.html import remove_tags
import html
from Test.items import Feed
from Test.settings import logger
from  Test.spiders.Central import Central
import hashlib

class Aajtak(Central):

    name="aajtak"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item    =   Feed()

        for data in response.css("item"):
            try:
                item['title']   =   html.unescape(data.css('item>title::text').get())
            except:
                item['title']   =   None

            try:
                link            =   data.css('item>link::text').get()
                item['link']    =   link
                result          =   hashlib.md5(link.encode())
                item['link_hash']=result.hexdigest()
            except:
                item['title']       =   None
                item['link_hash']   =   None

            try:
                item['description'] =   html.unescape(remove_tags(data.css('item>description::text').get()))
            except:
                item['description'] =   None

            try:
                item['pubDate']     =   data.css('item>pubDate::text').get()
            except:
                item['pubDate']     =   None
            logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
            
            yield item
