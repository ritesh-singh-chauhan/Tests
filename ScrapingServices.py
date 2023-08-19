from ProcessCrawler import *
from Connection import CentralSql, Redisconnection, Source, Domain
from Test.settings import REDIS_SETTINGS,logging,CUSTOM_CURRENT_TIME 
from rq import Queue
class ScrapingServices:

    def __init__(self):
        centralsqlobj       =   CentralSql()
        self.session        =   centralsqlobj.connect()
    def UsingRedis(self):
        try:
            logging.info(CUSTOM_CURRENT_TIME)
            query = self.session.query(Domain.name, Source.source, Source.statuss)\
               .join(Source, Source.domain_id == Domain.id)
               #.filter(Domain.id == 6)
            rows = query.all()
            
            q = Queue(connection=Redisconnection.redisconnection())
            print(rows)
            for row in rows:
                name,source,status= row[0], row[1], row[2]
                print(name,source,status)
                if status == 1:
                    processObj=ProcessCrawler()
                    job_name = "my_custom_job"
                    q.enqueue(processObj.feeds, args=(name,source)) 
        except Exception as error:
            logging.error(f"Error found in ScrapingServices{error}")
        finally:
            self.session.close()
        
obj_scraping=ScrapingServices()
obj_scraping.UsingRedis()

# import os
# import sys
# from pathlib import Path
# central=Path(__file__).resolve()
# processcrawler=os.path.join(central.parent,"Task/pipelines")
# print(sys.path)
# sys.path.insert(0,str(processcrawler))
# print(sys.path)