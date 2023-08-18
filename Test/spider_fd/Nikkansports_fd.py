
from Test.spiders.Central import Centralfd
from Test.items import FullDescription
import hashlib
from w3lib.html import remove_tags
import html

class Nikkansports_fd(Centralfd):
    name="nikkansports_fd"

    def parse(self,response):
        item=FullDescription()
        response.selector.remove_namespaces()
        st=remove_tags("".join(response.xpath("//section[@id='articleMain']/div/p//text()").getall()))
        print(st)
        link=self.url
        result=hashlib.md5(link.encode())
        try:
            item['link_hash']=result.hexdigest()
        except:
            item['link_hash']=''
        try:
            item['fulldescription']=html.unescape(st)
        except:
            item['fulldescription']=''
        yield item
