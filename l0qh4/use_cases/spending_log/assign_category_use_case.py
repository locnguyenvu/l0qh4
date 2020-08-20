import l0qh4

from ...spending.log import Log
from ...repository import SpendingLogRepository

class AssignCategoryUseCase:

    def __init__(self):
        self.__spendingcategories = l0qh4.get('spendingcategories')
        self.__spendinglog_repository = l0qh4.factory('spendinglog_repository')
        self.__lwscm_repository = l0qh4.get('languagewordspendingcategorymap_repository')

    def execute(self, log: Log, params: dict):
        category_id = params['category_id']
        category_name = self.__spendingcategories.get_name(category_id)
        log.set_category_id(category_id)
        self.__spendinglog_repository.save(log)

        for word in log.get_subject_words():
            wordcate = self.__lwscm_repository.find_first(
                    word = word,
                    category_id = category_id 
            )
            if wordcate is not None:
                wordcate.score += 1 
                self.__lwscm_repository.update(wordcate)
            else:
                self.__lwscm_repository.add(
                        word = word,
                        category_id = category_id,
                        category_name = category_name,
                        score = 1)

