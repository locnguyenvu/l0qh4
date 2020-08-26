from abc import ABCMeta, abstractmethod

from sqlalchemy import and_, Boolean, Column, DateTime, Integer, String
from .database import DB
from .orm_model import OrmModel
from .domain_model import DomainModel

class Repository(metaclass=ABCMeta):

    def __init__(self, database: DB):
        self._session = database.get_session()

    @classmethod
    @property 
    def ormclass(cls):
        return cls.ormclass 

    @classmethod
    @property 
    def domainclass(cls):
        return cls.domainclass

    def convert(self, resultset):
        if self.domainclass is None:
            return resultset
        if isinstance(resultset, OrmModel):
            model = self.domainclass().from_dict(resultset.to_dict())
            del resultset
            return model
        elif isinstance(resultset, list):
            return [ self.domainclass().from_dict(row.to_dict()) for row in resultset ]

    def _querybuilder(self):
        querybuilder = self._session.query(self.ormclass)
        return querybuilder

    def build_filter(self, **kwargs):
        querybuilder = self._querybuilder()
        for key, value in kwargs.items():
            if getattr(self.ormclass, key, None) is None:
                continue
            querybuilder = querybuilder.filter(getattr(self.ormclass, key) == value)
        return querybuilder

    def find_all(self, **kwargs):
        query = self.build_filter(**kwargs)
        result = query.all()
        return self.convert(result)

    def find_first(self, **kwargs):
        query = self.build_filter(**kwargs)
        result = query.first()
        return self.convert(result)

