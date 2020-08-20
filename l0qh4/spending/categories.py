from ..repository.spending_category import SpendingCategoryRepository

class Categories:

    def __init__(self, spendingcategory_repository: SpendingCategoryRepository):
        self.__data = spendingcategory_repository.listall()

    def get_name(self, catid: int):
        for category in self.__data:
            if category.id == catid:
                return category.name
        return None

    def get_id(self, catname: str):
        for category in self.__data:
            if category.name == catname:
                return category.id
        return None

    def listall(self):
        return self.__data

    def list_byids(self, ids: list):
        result = list()
        for category in self.__data:
            if category.id in ids:
                result.append(category)
        return result
