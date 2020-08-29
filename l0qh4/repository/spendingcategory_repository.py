from .orm_model.spending_category import SpendingCategory
from ..shared.repository import Repository

class SpendingCategoryRepository(Repository):

    ormclass = SpendingCategory

    domainclass = None
