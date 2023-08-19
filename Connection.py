from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from Test.settings import DB_SETTINGS, logging
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from Test.settings import REDIS_SETTINGS
from redis import Redis
Base = declarative_base()

class Domain(Base):

    __tablename__   =   'domain'

    id              =   Column(Integer, primary_key=True)
    name            =   Column(String)
    domain          =   Column(String)
    title           =   Column(String)
    description     =   Column(String)
    status          =   Column(Integer)
    fdstatus        =   Column(Integer)

class Source(Base):

    __tablename__ = 'source'
    
    id        =     Column(Integer, primary_key=True)
    domain_id =     Column(Integer, ForeignKey('domain.id'))
    source    =     Column(String)
    language  =     Column(String)
    country   =     Column(String)
    category  =     Column(String)
    status    =     Column(Integer)

class Redisconnection:

    def redisconnection():
        redis_conn = Redis(
                host    =   REDIS_SETTINGS["REDIS_HOST"], 
                port    =   REDIS_SETTINGS["REDIS_PORT"], 
                db      =   REDIS_SETTINGS["REDIS_DB"]
            )
        try:
            redis_conn.ping()
            logging.info('Redis connected Successfully')
            return redis_conn
        except Exception as redis_error:
            logging.error(f"Error while checking Redis connection: {redis_error}")

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
            logging.info("MySQL is connected")
            return self.Session()
        
        except Exception as e:

            logging.error("Error while connecting to MySQLAlchemy:", str(e))

    def get_database_url(self):
        return f"mysql+mysqlconnector://{DB_SETTINGS['USER']}:{DB_SETTINGS['PASSWORD']}@{DB_SETTINGS['HOST']}:{DB_SETTINGS['PORT']}/{DB_SETTINGS['DATABASE']}"