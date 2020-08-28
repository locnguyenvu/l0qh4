from ..log import Log
from ...repository.spendinglog_repository import SpendingLogRepository

class AddLogService(object):

    def __init__(self, sl_repository: SpendingLogRepository):
        self._sl_repository = sl_repository

    def execute(self, params: dict):
        log = Log(
            subject = params['subject'], 
            amount = params['amount'], 
            payment_method = params['payment_method'], 
            transaction_type = params['transaction_type'], 
            telegram_message_id = params['telegram_message_id'], 
            created_by = params['created_by'], 
            spending_category_id = None 
        )
        log = self._sl_repository.store(log)
        return log
