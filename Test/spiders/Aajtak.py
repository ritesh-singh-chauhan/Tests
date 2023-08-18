from w3lib.html import remove_tags
import html
from Test.items import TestItem
from  Test.spiders.Central import Central
import hashlib
class Aajtak(Central):
    name="aajtak"
    def parse(self,response):
        item=TestItem()
        for data in response.css("item"):
            try:
                item['title']=html.unescape(data.css('item>title::text').get())
            except:
                item['title']=''
            try:
                link=data.css('item>link::text').get()
                item['link']=link
                result = hashlib.md5(link.encode())
                item['link_hash']=result.hexdigest()
            except:
                item['title']=''
                item['link_hash']=''
            try:
                item['description']=html.unescape(remove_tags(data.css('item>description::text').get()))
            except:
                item['description']=''
            try:
                item['pubDate']=data.css('item>pubDate::text').get()
            except:
                item['pubDate']=''
            yield item
