import hashlib
from Test.settings import logger
from w3lib.html import remove_tags
from Test.items import FullDescription
from Test.spiders.Central import Centralfd

class Almasalahfd(Centralfd):

    name="almasalah_fd"
    
    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item=FullDescription()
        response.selector.remove_namespaces()
        l=response.xpath("//div[@class='entry-content read-details']/p/text()").getall()
        st="".join(l)
        link=self.url
        result=hashlib.md5(link.encode())
        item['link_hash']=result.hexdigest()
        item['fulldescription']=remove_tags(st)
        logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")

        yield item
