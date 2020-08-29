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
        logid_search = re.search(r'\d+', self.update.message.text)
        if logid_search is None:
            return None
        log = self._sl_repository.find_first(id=int(logid_search.group(0)))
        return log

    def process(self):

        log = self.find_log()
        if log is None:
            self.reply('!e404 - log not exists')
            return

        listservice = ListProposedCategoriesService()
        proposed_categories = listservice.execute(log)

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
