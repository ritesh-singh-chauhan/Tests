
from Test.settings import logger
from Test.spiders.Central import Centralfd
from Test.items import FullDescription
import hashlib
from w3lib.html import remove_tags
import html

class Aajtak_fd(Centralfd):
    
    name="aajtak_fd"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item    =   FullDescription()
        response.selector.remove_namespaces()
        st      =   remove_tags("".join(response.xpath("//div[@class='content-area']//div/*[self::p or self::h2]/text()").getall()))
        link    =   self.url
        result  =   hashlib.md5(link.encode())
        item['link_hash']       =   result.hexdigest()
        item['fulldescription'] =   html.unescape(st)
        logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")

        yield item