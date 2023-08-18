import html
import hashlib
from w3lib.html import remove_tags
from Test.spiders.Central import Central
from Test.items import TestItem
from Test.settings import logging, CUSTOM_CURRENT_TIME
class FranceAmerica(Central):


    name="franceamerica"

    def parse(self,response):

        try: 
            if response.status !=200:
                logging.error(f"response.status: {response.status}, Current Time: {CUSTOM_CURRENT_TIME}")            
            else:
                item=TestItem()
                response.selector.remove_namespaces()
                for data in response.xpath("//item"):
                    logging.info("Step 6 Recieved response from the Engine Parsing started")
                    try:
                        item['title'] = data.xpath("title/text()").get()
                    except:
                        item['title'] = None
                    try:
                        link=data.xpath("link/text()").get()
                        item['link']  = link
                    except:
                        item['link']  = None
                    try:
                        result        = hashlib.md5(link.encode())
                        item['link_hash']  = result.hexdigest()
                    except:
                        item['link_hash']  = None
                    try:
                        content=data.xpath("description/text()").get()
                        item['description'] = html.unescape(remove_tags(content))
                    except:
                        item['description'] = None
                    try:
                        item['pubDate']     = data.xpath("pubDate/text() | pubdate/text()").get()
                    except:
                        item['pubDate']     = None
                
                    if item['title'] != None and item['link'] != None and item['pubDate'] != None: 
                        logging.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
                        yield item

        except Exception as e:
            logging.error(str(e))