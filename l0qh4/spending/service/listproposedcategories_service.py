import l0qh4

from ..log import Log
from .service import Service
from ...repository.spendingwordcategory_repository import SpendingWordCategoryRepository

class ListProposedCategoriesService(Service):

    def __init__(self):
        db = l0qh4.get('db')
        self._swc_repository = SpendingWordCategoryRepository(db)

    def execute(self, log: Log, configs: dict = {}):
        flag_listall = configs.get('list_all', False)
        wordcategorymap = dict()
        for word in log.get_subject_words():
            wcmapresultset = self._swc_repository.find_all(word = word)
            for wcmap in wcmapresultset:
                if wcmap.category_id in wordcategorymap:
                    wordcategorymap[wcmap.category_id] += wcmap.score
                else:
                    wordcategorymap[wcmap.category_id] = wcmap.score

        categories = l0qh4.get('spendingcategories')

        if len(wordcategorymap) == 0 or flag_listall == True:
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

        return proposed_categories 
