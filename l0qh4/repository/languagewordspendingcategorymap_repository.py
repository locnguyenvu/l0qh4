from datetime import datetime
from .orm_model.language_word_spending_category_map import LanguageWordSpendingCategoryMap
from ..shared.repository import Repository

class LanguageWordSpendingCategoryMapRepository(Repository):

    ormclass = LanguageWordSpendingCategoryMap

    domainclass = None

    def add(self, word: str, category_id: int, category_name: str, score: int):
        instance = self.orm_class()()
        instance.word = word
        instance.category_id = category_id
        instance.score = score
        instance.created_at = datetime.now()
        instance.updated_at = datetime.now()
        self._session.add(instance)
        self._session.commit()

