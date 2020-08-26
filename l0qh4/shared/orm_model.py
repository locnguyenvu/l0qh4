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



