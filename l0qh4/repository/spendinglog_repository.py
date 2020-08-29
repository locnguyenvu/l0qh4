from ..utils import DateTimeUtil
from datetime import datetime
from sqlalchemy import and_
from l0qh4.shared import repository
from .orm_model.spending_log import SpendingLog
from ..spending.log import Log

class SpendingLogRepository(repository.Repository):

    domainclass = Log
    
    ormclass = SpendingLog

    def store(self, log: Log):
        orm = self.ormclass()
        orm.id = log.get_id()
        orm.subject = log.get_subject()
        orm.amount = log.get_amount()
        orm.payment_method = log.get_payment_method()
        orm.transaction_type = log.get_transaction_type()
        orm.spending_category_id = log.get_category_id()
        orm.telegram_message_id = log.get_telegram_message_id()
        orm.created_by = log.get_created_by()
        orm.created_at = log.get_created_at()
        orm.updated_at = datetime.now()
        if orm.id is not None:
            orm = self._session.merge(orm)
        elif orm.created_at is None:
            orm.created_at = datetime.now()
        self._session.add(orm)
        self._session.commit()
        log.set_id(orm.id)
        return log

    
    def find_intimerange(self, timetext:str):
        datetimerange = DateTimeUtil.datetime_range(timetext)
        if len(datetimerange) == 0:
            return None
        resultset = self._session.query(SpendingLog).filter(
                and_(   
                    SpendingLog.created_at > datetimerange[0],
                    SpendingLog.created_at < datetimerange[1]
            )).all()
        return self.convert(resultset)
