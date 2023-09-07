from ProcessCrawler import *
from Connection import CentralSql, Redisconnection, Source, Domain
from Test.settings import REDIS_SETTINGS,logger,CUSTOM_CURRENT_TIME 
from rq import Queue
from rq.job import Job 

class ScrapingServices:

    def __init__(self):
        centralsql_obj       =   CentralSql()
        self.session         =   centralsql_obj.connect()
        
    def UsingRedis(self):
        try:
            logger.info(CUSTOM_CURRENT_TIME)
            sql_query   =   self.session.query(Domain.name, Source.source, Source.status)\
               .join(Source, Source.domain_id   ==  Domain.id)

            rows        =   sql_query.all()
            redis_conn  =   Redisconnection.redisconnection()
            redis_queue =   Queue(connection=redis_conn)
            job_count   =   0
            for row in rows:
                job_count=  job_count+1
                name,source,status  =   row[0], row[1], row[2]
                logger.info(f"{name}, {source}, {status}")
                if status   ==  1:
                    processObj=ProcessCrawler()
                    job_name    =   str(job_count)+name
                    job         =   redis_queue.enqueue(processObj.feeds, args=(name,source),job_name=job_name)
                    job         =   Job.fetch(job.id, connection=redis_conn)
                    # job.meta['job_name'] = 'my_updated_job_name'
                    job.save()
        except Exception as error:
            logger.error(f"Error found in ScrapingServices{error}")

        finally:
            self.session.close()
        
obj_scraping    =   ScrapingServices()
obj_scraping.UsingRedis()
# import os
# import sys
# from pathlib import Path
# central=Path(__file__).resolve()
# processcrawler=os.path.join(central.parent,"Task/pipelines")
# print(sys.path)
# sys.path.insert(0,str(processcrawler))
# print(sys.path)