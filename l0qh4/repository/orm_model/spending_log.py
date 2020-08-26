from sqlalchemy import Boolean, Column, DateTime, Integer, String
from l0qh4.shared.orm_model import OrmModel

class SpendingLog(OrmModel):
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
