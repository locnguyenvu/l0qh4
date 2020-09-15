from sqlalchemy import Boolean, Column, DateTime, Integer, String
from ...shared.orm_model import OrmModel

class Config(OrmModel):

    __tablename__ = 'config'

    id = Column(
            Integer, 
            primary_key=True)

    path = Column(
            String(255),
            nullable=False)

    value = Column(
            String(255),
            nullable=False)

    created_at = Column(
            DateTime,
            nullable=True)

    updated_at = Column(
            DateTime,
            nullable=True)
