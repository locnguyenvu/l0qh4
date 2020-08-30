import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .handler import Handler
from ...repository.spendinglog_repository import SpendingLogRepository
from ...spending.service.addlog_service import AddLogService
from ...spending.service.listproposedcategories_service import ListProposedCategoriesService
from ...spending.helper import LogMessage


class AddLogHandler(Handler):

    def process(self):
        """ Add new log """
        chat_info = self.update.message.chat
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

        self.update.message.reply_text(f'{log.get_subject()}', reply_markup=reply_markup)

        return

