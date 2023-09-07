
from Test.spiders.Central import Centralfd
from Test.items import FullDescription
import hashlib
from w3lib.html import remove_tags
import html
from Test.settings import logger
class FranceAmerica_fd(Centralfd):


    name    =   "franceamerica_fd"

    def parse(self,response):

        logger.info("Step 6 Recieved response from the Engine Parsing started")
        item    =   FullDescription()
        response.selector.remove_namespaces()
        st      =   remove_tags("\n".join(response.xpath("//div[@class='elementor-section-wrap']//h2 | //div[@class='elementor-section-wrap']//p").getall()))
        result  =   hashlib.md5(self.url.encode())

        try:
            item['link_hash']       =   result.hexdigest()

        except:
            item['link_hash']       =   None

        try:
            item['fulldescription'] =   html.unescape(st)

        except:
            item['fulldescription'] =   None 

        logger.info("Step 7 Sendings item to the engine then ITEM_PIPELINE")
        
        yield item