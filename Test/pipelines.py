# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient
from ProcessCrawler import *
from Test.items import Feed,FullDescription
from Connection import CentralSql,Redisconnection,Domain,Source
from Test.settings import REDIS_SETTINGS,logger
from rq import Queue

dict_status       =   dict()
sql_obj           =   CentralSql()    
redis_queue       =   Queue(connection    =   Redisconnection.redisconnection())


class MongoDBPipeline:
    
    def __init__(self, mongo_uri, mongo_db):
        self.client     =   MongoClient(mongo_uri)
        self.db         =   self.client[mongo_db]
        #self.collection =   self.db["france_america"]
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db  = crawler.settings.get('MONGO_DATABASE')
        )
    # def open_spider(self, spider):
    #     pass

    def process_item(self, item, spider):
        
        if isinstance(item,Feed):
            if item['title']    ==  None or item["link"]  ==  None or item['description']   ==  None or item['pubDate']   ==  None:
                pass
            else:
                logger.info("Step-8 The Engine sends processed items to Item Pipelines, then send processed Requests to the Scheduler and asks for possible next Requests to crawl.")
                link        =   item['link']
                spider_fd   =   spider.name+"_fd"   
                try:

                    if spider.name not in dict_status.keys():
                        session     =   sql_obj.connect()    
                        query       =   session.query(Domain.fdstatus).join(Source, Source.domain_id == Domain.id).filter( Domain.name == spider.name )
    
                        fdstatus    =   query.all()
                        dict_status[spider.name]= fdstatus[0][0]
                        session.close()
                        logger.info("Status of the FD",fdstatus)

                    if dict_status[spider.name]   ==  1:
                        processcrawler_obj  =   ProcessCrawler()
                        redis_queue.enqueue(processcrawler_obj.feed_fd(spider_fd,link)) 
                                       
                except Exception as error:
                    logger.error(f"Error Found in SQL Query pipeline:{error}")

            
                self.db[spider.name].insert_one(dict(item))

        if isinstance(item,FullDescription):
            try:
                logger.info("Step-8 The Engine sends processed items to Item Pipelines, then send processed Requests to the Scheduler and asks for possible next Requests to crawl.")
                self.db[spider.name[:-3]].update_one({"link_hash":item['link_hash']},{"$set":{"Full_Description":item['fulldescription']}})
            except Exception as e:
                logger.info("Unable to update")
        else:
            pass 
        
    def close_spider(self, spider):
        self.client.close()