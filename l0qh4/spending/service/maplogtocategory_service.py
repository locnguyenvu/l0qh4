import l0qh4

from .service import Service
from ..log import Log
from ...repository.orm_model.spending_word_category import SpendingWordCategory
from ...repository.spendinglog_repository import SpendingLogRepository
from ...repository.spendingwordcategory_repository import SpendingWordCategoryRepository

class MapLogToCategoryService(Service):

    def __init__(self):
        db = l0qh4.get('db')
        self._sl_repository = SpendingLogRepository(db)
        self._swc_repository = SpendingWordCategoryRepository(db)
        self._scategories = l0qh4.get('spendingcategories')


    def execute(self, log: Log, category_id: int):
        if not self._scategories.exist(int(category_id)):
            return
        log.set_category_id(category_id)
        self._sl_repository.store(log)

        for word in log.get_subject_words():
            wordcat = self._swc_repository.find_first(word = word, category_id = category_id)
            if wordcat is None:
                wordcat = SpendingWordCategory.new(
                    word = word,
                    category_id = category_id,
                    category_name = self._scategories.get_name(int(category_id)),
                    score = 1
                )
            else:
                wordcat.score += 1

            self._swc_repository.save(wordcat)
