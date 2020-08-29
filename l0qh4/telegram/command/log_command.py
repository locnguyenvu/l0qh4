import l0qh4

from .command import Command
from ...spending.service.addlog_service import AddLogService
from ...spending.helper import LogMessage

class LogCommand(Command):

    def process(self):
        log_message = LogMessage(self.get_messagecontent())

        db = l0qh4.get('db')
        addlog_service = AddLogService()
        log = addlog_service.execute({
            "subject" : log_message.subject(),
            "amount" : log_message.amount(),
            "payment_method" : log_message.payment_method(),
            "transaction_type" : log_message.transaction_type(),
            "created_by" : self.username,
            "telegram_message_id" : self.message_id 
        })

        self.reply(f"hello loc {log.get_id()}")
