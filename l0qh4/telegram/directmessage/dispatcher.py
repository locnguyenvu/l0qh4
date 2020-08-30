import l0qh4
import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .addlog_handler import AddLogHandler
from ...repository.spendinglog_repository import SpendingLogRepository
from ...spending.service.addlog_service import AddLogService
from ...spending.service.listproposedcategories_service import ListProposedCategoriesService
from ...spending.helper import LogMessage

class Dispatcher(object):

    def __init__(self, chatgroup_ids:str):
        self.__chatgroup_ids = [ int(cgid) for cgid in chatgroup_ids.split(',') ]

    def __call__(self, update : telegram.Update, context):
        self.update = update
        self.context = context
        if not self.is_authorized():
            return

        if self.update.message is not None:
            handler = AddLogHandler(update, context)
            handler.process()
            return

        if self.update.edited_message is not None:
            self._editlog()
            return

    def is_authorized(self) -> bool:
        tlg_username = self.username
        if tlg_username is None:
            return False
        users = l0qh4.get('users')
        if not users.is_active(telegram_username = tlg_username):
            return False
        chat_info = self.update.message.chat
        if chat_info.type == 'group' and chat_info.id not in self.__chatgroup_ids:
            return False
        return True

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
        chat_info = self.update.message.chat
        if chat_info.type == 'group' and chat_info.id not in self.__chatgroup_ids:
            return
        if chat_info.type == 'private' and self.update.message.forward_date is None:
            return

        log_message = LogMessage(self.update.message.text)
        if not log_message.is_valid():
            return
        addlog_service = AddLogService()
        addlog_params = {
            "subject" : log_message.subject(),
            "amount" : log_message.amount(),
            "payment_method" : log_message.payment_method(),
            "transaction_type" : log_message.transaction_type(),
            "created_by" : self.username,
            "telegram_message_id" : self.message_id 
        }
        if self.update.message.forward_date != None:
            addlog_params["created_at"] = self.update.message.forward_date

        log = addlog_service.execute(addlog_params)
        
        lspc_service = ListProposedCategoriesService()
        proposed_categories = lspc_service.execute(log)
        keyboard = [
                [
                    InlineKeyboardButton(
                        f"{category['name']}", 
                        callback_data=f"MapSlCategoryCallbackQuery|logid={log.get_id()},categoryid={category['id']}")
                ]
                for category in proposed_categories
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        self.context.bot.send_message(
                chat_id = self.update.effective_chat.id,
                text = f'{log.get_subject()}',
                reply_markup=reply_markup)

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
