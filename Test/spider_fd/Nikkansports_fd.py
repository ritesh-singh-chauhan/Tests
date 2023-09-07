from Test.settings import logger
from Test.spiders.Central import Centralfd
from Test.items import FullDescription
import hashlib
from w3lib.html import remove_tags
import html

class Nikkansports_fd(Centralfd):

    name    =   "nikkansports_fd"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item    =   FullDescription()
        response.selector.remove_namespaces()
        st      =   remove_tags("".join(response.xpath("//section[@id='articleMain']/div/p//text()").getall()))
        link    =   self.url
        result  =   hashlib.md5(link.encode())
        try:
            item['link_hash']   =   result.hexdigest()
        except:
            item['link_hash']   =   None 
        try:
            item['fulldescription'] =   html.unescape(st)
        except:
            item['fulldescription'] =   None 
        logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
        
        yield item