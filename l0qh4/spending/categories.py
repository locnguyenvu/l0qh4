from ..repository.spendingcategory_repository import SpendingCategoryRepository

class Categories:

    def __init__(self, sc_repository: SpendingCategoryRepository):
        self._sc_repository = sc_repository
        self.__data = self._sc_repository.find_all()

    def get_name(self, catid: int):
        for category in self.__data:
            if category.id == catid:
                return category.name
        return None

    def get_displayname(self, catid: int):
        for category in self.__data:
            if category.id == catid:
                return category.name if not category.display_name else category.display_name
        return 'Unknown' 

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

    def exist(self, id: int) -> bool :
        for category in self.__data:
            if category.id == id:
                return True
        return False

    def get(self, id: int):
        from pprint import pprint
        for cat in self.__data:
            if int(cat.id) == int(id):
                return cat
        return None
