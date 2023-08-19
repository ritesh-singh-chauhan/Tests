# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient
from ProcessCrawler import *
from Test.items import TestItem,FullDescription
from Connection import CentralSql,Redisconnection,Domain,Source
from Test.settings import REDIS_SETTINGS,logging
from rq import Queue

d       =   {}
sql_obj =   CentralSql()    
r       =   Queue(connection    =   Redisconnection.redisconnection())
class MongoDBPipeline:
    
    def __init__(self, mongo_uri, mongo_db):
        self.client     =   MongoClient(mongo_uri)
        self.db         =   self.client[mongo_db]
        self.collection =   self.db["france_america"]
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db  = crawler.settings.get('MONGO_DATABASE')
        )
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        
        if isinstance(item,TestItem):
            logging.info("Step-8 The Engine sends processed items to Item Pipelines, then send processed Requests to the Scheduler and asks for possible next Requests to crawl.")
            link        =   item['link']
            spider_fd   =   spider.name+"_fd"   
            try:

                if spider.name not in d.keys():
                    session     =   sql_obj.connect()    
                    query       =   session.query(Domain.fdstatus).join(Source, Source.domain_id == Domain.id).filter( Domain.name == spider.name )
    
                    fdstatus    =   query.all()
                    d[spider.name]= fdstatus[0][0]
                    session.close()
                    logging.info("Status of the FD",fdstatus)

                if d[spider.name]   ==  1:
                    process_obj  =   ProcessCrawler()
                    r.enqueue(process_obj.feed_fd(spider_fd,link)) 
                                       
            except Exception as error:
                logging.error(f"Error Found in SQL Query pipeline:{error}")
            
            self.collection.insert_one(dict(item))

        if isinstance(item,FullDescription):
            try:
                logging.info("Step-8 The Engine sends processed items to Item Pipelines, then send processed Requests to the Scheduler and asks for possible next Requests to crawl.")
                self.collection.update_one({"link_hash":item['link_hash']},{"$set":{"Full_Description":item['fulldescription']}})
            except Exception as e:
                logging.info("Unable to update")
        #return item 
        
    def close_spider(self, spider):
        self.client.close()