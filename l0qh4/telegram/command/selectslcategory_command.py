import l0qh4
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .command import Command
from ...spending.service.listproposedcategories_service import ListProposedCategoriesService
from ...repository.spendinglog_repository import SpendingLogRepository
from ...repository.spendingwordcategory_repository import SpendingWordCategoryRepository 

class SelectSlCategoryCommand(Command):

    def __init__(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))
        self._swc_repository = SpendingWordCategoryRepository(l0qh4.get('db'))

    def find_log(self):
        if self.update.message.reply_to_message is None:
            return
        log = self._sl_repository.find_first(telegram_message_id=int(self.update.message.reply_to_message.message_id))
        return log

    def process(self):

        log = self.find_log()
        if log is None:
            self.reply('!e404 - log not exists')
            return

        listservice = ListProposedCategoriesService()
        proposed_categories = listservice.execute(log, {"list_all": True})

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
