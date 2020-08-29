from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm.state import InstanceState
from sqlalchemy import MetaData

Base = declarative_base()

class OrmModel(Base):

    __abstract__ = True

    def to_dict(self):
        attrdict = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, InstanceState):
                continue
            attrdict[key] = value
        return attrdict

    @classmethod
    def new(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        if (hasattr(instance, 'created_at')):
            setattr(instance, 'created_at', datetime.now())
        return instance
