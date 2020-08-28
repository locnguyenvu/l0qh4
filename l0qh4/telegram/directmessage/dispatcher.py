import l0qh4
import telegram

from ...repository.spendinglog_repository import SpendingLogRepository
from ...spending.service.addlog_service import AddLogService
from ...spending.helper import LogMessage

class Dispatcher(object):

    def __init__(self, chatgroup_ids:str):
        self.__chatgroup_ids = [ int(cgid) for cgid in chatgroup_ids.split(',') ]

    def __call__(self, update : telegram.Update, context):
        self.update = update
        self.context = context
        if not self.is_authorized():
            return
        db = l0qh4.get('db')
        if self.update.message is not None:
            self._addlog()
            return

        if self.update.edited_message is not None:
            self._editlog()
            return

    def is_authorized(self) -> bool:
        tlg_username = self.username
        if tlg_username is None:
            return False
        users = l0qh4.get('users')
        return users.is_active(telegram_username = tlg_username)

    @property
    def username(self):
        tlg_username = None
        if self.update.message is not None:
            tlg_username = self.update.message.from_user.username
        elif self.update.edited_message is not None:
            tlg_username = self.update.edited_message.from_user.username
        return tlg_username

    @property
    def message_id(self):
        return self.update.message.message_id

    @property
    def effective_chat_id(self):
        return self.update.effective_chat.id

    def reply(self, text: str, parse_mode = None):
        self.bot.send_message(
                chat_id = self.effective_chat_id,
                text = text,
                parse_mode = parse_mode)

    def _addlog(self):
        """ Add new log """
        db = l0qh4.get('db')
        addlog_service = AddLogService(sl_repository = SpendingLogRepository(db))
        chat_info = self.update.message.chat
        log_message = LogMessage(self.update.message.text)
        if chat_info.type == 'group' and chat_info.id not in self.__chatgroup_ids:
            return

        addlog_params = {
            "subject" : log_message.subject(),
            "amount" : log_message.amount(),
            "payment_method" : log_message.payment_method(),
            "transaction_type" : log_message.transaction_type(),
            "created_by" : self.username,
            "telegram_message_id" : self.message_id 
        }
        if chat_info.type == 'private' and self.update.message.forward_date != None:
            addlog_params["created_at"] = self.update.message.forward_date

        log = addlog_service.execute(addlog_params)
        return

    def _editlog(self):
        """ Update on edit message """
        db = l0qh4.get('db')
        sl_repository = SpendingLogRepository(db)

        log = sl_repository.find_first(telegram_message_id = self.update.edited_message.message_id)
        log_message = LogMessage(self.update.edited_message.text)
        
        if log is None or not log_message.is_valid():
            return

        log.set_subject(log_message.subject())
        log.set_amount(log_message.amount())
        log.set_payment_method(log_message.payment_method())
        log.set_transaction_type(log_message.transaction_type())
        sl_repository.store(log)
