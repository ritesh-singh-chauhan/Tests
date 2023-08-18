import hashlib
from w3lib.html import remove_tags
from Test.items import FullDescription
from ProcessCrawler import *
from Test.spiders.Central import Centralfd
class Bahazani_fd(Centralfd):
    name="bahazani_fd"

    def parse(self,response):
        item=FullDescription()
        response.selector.remove_namespaces()
        st="".join(response.xpath("//div[@class='tdb-block-inner td-fix-index']/p/text() | //div[@class='details-news']/p/text() | \
                                  //div[@class='tdb-block-inner td-fix-index']//div//text()").getall())
        link=self.url
        result=hashlib.md5(link.encode())
        item['link_hash']=result.hexdigest()
        item['fulldescription']=remove_tags(st)
        yield item