import l0qh4
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .command import Command
from ...repository.spendinglog_repository import SpendingLogRepository
from ...repository.languagewordspendingcategorymap_repository import LanguageWordSpendingCategoryMapRepository 

class SelectSlCategoryCommand(Command):

    def __init__(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))
        self._lwscm_repository = LanguageWordSpendingCategoryMapRepository(l0qh4.get('db'))

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

        wordcategorymap = dict()
        for word in log.get_subject_words():
            wcmapresultset = self._lwscm_repository.find_all(word = word)
            for wcmap in wcmapresultset:
                if wcmap.category_id in wordcategorymap:
                    wordcategorymap[wcmap.category_id] += wcmap.score
                else:
                    wordcategorymap[wcmap.category_id] = wcmap.score

        categories = l0qh4.get('spendingcategories')

        if len(wordcategorymap) == 0:
            proposed_categories = [ 
                    {"id": category.id, "name": category.name, "display_name": category.display_name}
                    for category in categories.listall()
            ]
        else:
            wordcategorymap = sorted(wordcategorymap.items(), reverse=True, key=lambda x: x[1])
            proposed_categories = [ 
                    {"id": category.id, "name": category.name, "display_name": category.display_name}
                    for category in categories.list_byids([ca[0] for ca in wordcategorymap])
            ]

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
