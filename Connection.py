from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from Test.settings import DB_SETTINGS, logger
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from Test.settings import REDIS_SETTINGS
from redis import Redis
Base = declarative_base()

class Domain(Base):

    __tablename__   =   'domain'

    id              =   Column("id", Integer, primary_key=True)
    name            =   Column("name", String)
    domain          =   Column("domain", String)
    title           =   Column("title", String)
    description     =   Column("description", String)
    status          =   Column("status", Integer)
    fdstatus        =   Column("fdstatus", Integer)

class Source(Base):

    __tablename__ = 'source'
    
    id        =     Column("id", Integer, primary_key=True)
    domain_id =     Column("domain_id", Integer, ForeignKey('domain.id'))
    source    =     Column("source", String)
    language  =     Column("language", String)
    country   =     Column("country", String)
    category  =     Column("category", String)
    status    =     Column("status", Integer)

class Redisconnection:

    def redisconnection():
        redis_conn = Redis(
                host    =   REDIS_SETTINGS["REDIS_HOST"], 
                port    =   REDIS_SETTINGS["REDIS_PORT"], 
                db      =   REDIS_SETTINGS["REDIS_DB"]
            )
        try:
            redis_conn.ping()
            logger.info('Redis connected Successfully')
            return redis_conn
        except Exception as redis_error:
            logger.error(f"Error while checking Redis connection: {redis_error}")

class CentralSql:
    def __init__(self):
        self.connection =   None
        self.engine     =   None
        self.Session    =   None
        self.session    =   None

    def connect(self):
        try:

            self.engine     =   create_engine(self.get_database_url())
            self.Session    =   sessionmaker(bind=self.engine)
            logger.info("MySQL is connected")
            return self.Session()
        
        except Exception as e:

            logger.error("Error while connecting to MySQLAlchemy:", str(e))

    def get_database_url(self):
        return f"mysql+mysqlconnector://{DB_SETTINGS['USER']}:{DB_SETTINGS['PASSWORD']}@{DB_SETTINGS['HOST']}:{DB_SETTINGS['PORT']}/{DB_SETTINGS['DATABASE']}"