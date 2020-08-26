from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DB(object):

    def __init__(self, url: str):
        engine = create_engine(url, echo = False)
        Session = sessionmaker(bind=engine)
        self.__engine = engine
        self.__session = Session()

    def get_engine(self):
        return self.__engine

    def get_session(self):
        return self.__session

    def session(self):
        return self.__session

    def engine(self):
        return self.__engine

