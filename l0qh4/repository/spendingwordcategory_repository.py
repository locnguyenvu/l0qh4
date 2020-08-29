from .orm_model.spending_word_category import SpendingWordCategory
from ..shared.repository import Repository

class SpendingWordCategoryRepository(Repository):

    ormclass = SpendingWordCategory

    domainclass = None
