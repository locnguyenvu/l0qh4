import l0qh4

from .service import Service
from ..log import Log
from ...repository.spendinglog_repository import SpendingLogRepository

class AddLogService(Service):

    def __init__(self):
        db = l0qh4.get('db')
        self._sl_repository = SpendingLogRepository(db)

    def execute(self, params: dict):
        log = Log(
            subject = params['subject'], 
            amount = params['amount'], 
            payment_method = params['payment_method'], 
            transaction_type = params['transaction_type'], 
            telegram_message_id = params['telegram_message_id'], 
            created_by = params['created_by'], 
            spending_category_id = None,
            created_at = params.get('created_at', None)
        )
        log = self._sl_repository.store(log)
        return log
