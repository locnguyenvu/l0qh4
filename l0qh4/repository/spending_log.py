import l0qh4

from datetime import datetime
from sqlalchemy import and_, Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import select
from . import Base, BaseRepository, DateTimeUtil

class SpendingLog(Base):

    __tablename__ = 'spending_log'

    id = Column(
            Integer, 
            primary_key=True)

    subject = Column(
            String, 
            nullable = True)

    amount = Column(
            Integer, 
            nullable = True)

    payment_method = Column(
            String,
            nullable = True)

    transaction_type = Column(
            String,
            nullable = True)

    telegram_message_id = Column(
            Integer,
            nullable = False)

    created_by = Column(
            String,
            nullable = False)

    spending_category_id = Column(
            String,
            nullable = True)

    created_at = Column(
            DateTime,
            nullable = True)

    updated_at = Column(
            DateTime,
            nullable = False)

    def __repr__(self):
        return f"<(id={self.id}, subject={self.subject}, amount={self.amount})>"

    @classmethod
    def new(cls,
            subject: str,
            amount: int,
            payment_method: str,
            transaction_type: str,
            created_by: str,
            telegram_message_id: str):
        instance = cls()
        instance.subject = subject
        instance.amount = amount
        instance.payment_method = payment_method
        instance.transaction_type = transaction_type
        instance.created_by = created_by
        instance.telegram_message_id = telegram_message_id
        instance.created_at = datetime.now()
        instance.updated_at = datetime.now()
        return instance

class SpendingLogRepository(BaseRepository):

    @classmethod
    def orm_class(cls):
        return SpendingLog

    def listall_intimerange(self, timetext:str):
        datetimerange = DateTimeUtil.datetime_range(timetext)
        if len(datetimerange) == 0:
            return None
        resultset = self._session.query(SpendingLog).filter(
                and_(   
                    SpendingLog.created_at > datetimerange[0],
                    SpendingLog.created_at < datetimerange[1]
            )).all()
        return resultset

    def add(self,
            subject: str,
            amount: int,
            payment_method: str,
            transaction_type: str,
            created_by: str,
            telegram_message_id: str,
            created_at = None
    ):
        orm_object = self.orm_class().new(
            subject = subject,
            amount = amount,
            payment_method = payment_method,
            transaction_type = transaction_type,
            created_by = created_by,
            telegram_message_id = telegram_message_id)
        if created_at is not None:
            mapping_class.created_at = created_at
        self._session.add(orm_object)
        self._session.commit()
        return orm_object

    def save(self, entity):
        if entity.get_id() is not None:
            orm = self.find(entity.get_id())
            orm.subject = entity.get_subject()
            orm.amount = entity.get_amount()
            orm.spending_category_id = entity.get_category_id()
            orm.payment_method = entity.get_payment_method()
            orm.transaction_type = entity.get_transaction_type()
            self.update(orm)

