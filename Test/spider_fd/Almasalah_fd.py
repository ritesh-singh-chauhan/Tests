import scrapy
import hashlib
from w3lib.html import remove_tags
from Test.items import FullDescription
from Test.spiders.Central import Centralfd
class Almasalahfd(Centralfd):
    name="almasalah_fd"
    
    def parse(self,response):
        item=FullDescription()
        response.selector.remove_namespaces()
        l=response.xpath("//div[@class='entry-content read-details']/p/text()").getall()
        st="".join(l)
        link=self.url
        result=hashlib.md5(link.encode())
        item['link_hash']=result.hexdigest()
        item['fulldescription']=remove_tags(st)
        yield item
