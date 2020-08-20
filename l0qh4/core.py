import re

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()

class DB:
    
    def __init__(self, url:str):
        self.__engine = create_engine(url, echo=False)
        Session.configure(bind=self.__engine)
        self.__session = Session()

    def session(self):
        return self.__session

    def engine(self):
        return self.__engine


class BaseRepository:
   
    def __init__(self, db: DB):
        self._session = db.session()
        self._engine = db.engine()

    @classmethod
    def orm_class(cls) -> Base:
        return Base

    def find(self, id: int, entity_class = None) :
        orm_class = self.orm_class()
        result = self._session.query(orm_class).filter(orm_class.id == id).first()
        if entity_class is None:
            return result
        else:
            return entity_class.from_dict(self.orm_to_dict(result))

    def find_all(self, entity_class=None, **kwargs):
        orm_class = self.orm_class()
        query = self._session.query(orm_class)
        for key, value in kwargs.items():
            if getattr(orm_class, key, None) is None:
                continue
            query = query.filter(getattr(orm_class, key) == value)
        resultset = query.all()
        if entity_class is not None:
            return [
                    entity_class.from_dict(self.orm_to_dict(result))
                    for result in resultset
                ]
        else:
            return resultset

    def find_first(self, **kwargs):
        orm_class = self.orm_class()
        query = self._session.query(orm_class)
        for key, value in kwargs.items():
            if getattr(orm_class, key, None) is None:
                continue
            query = query.filter(getattr(orm_class, key) == value)
        result = query.first()
        return result

    def listall(self):
        resultset = self._session.query(self.orm_class()).all()
        return resultset

    def update(self, orm_object: Base):
        orm_object.updated_at = datetime.now()
        self._session.add(orm_object)
        self._session.commit()

    @staticmethod
    def orm_to_dict(orm_object: Base) -> dict:
        odict = dict()
        for attr in dir(orm_object.__class__):
            if re.match('(^_|metadata)', attr):
                continue
            odict[attr] = getattr(orm_object, attr)
        return odict

