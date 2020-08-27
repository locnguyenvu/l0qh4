from sqlalchemy import Boolean, Column, DateTime, Integer, String
from ...shared.orm_model import OrmModel

class User(OrmModel):

    __tablename__ = 'user'

    id = Column(
            Integer, 
            primary_key=True)

    telegram_username = Column(
            String, 
            nullable=False)

    telegram_userid = Column(
            Integer, 
            nullable=False)

    alias = Column(
            String, 
            nullable=True)

    is_active = Column(
            Boolean, 
            nullable=True)

    def __init__(
            self,
            telegram_username,
            telegram_userid,
            alias):
        self.telegram_username = telegram_username
        self.telegram_userid = telegram_userid
        self.alias = alias

    def __repr__(self):
        return f'<User(name={self.telegram_username}, is_active={self.is_active})>'
