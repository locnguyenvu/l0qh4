import l0qh4

from l0qh4.spending.log import Log

class ListProposedCategoryUseCase:

    def __init__(self):
        self.__lwscm_repository = l0qh4.get('languagewordspendingcategorymap_repository')
    
    def execute(self, spendinglog: Log, params:dict={}):
        listallflag = params.get('listall', False)
        wordcategorymap = dict()
        for word in spendinglog.get_subject_words():
            wcmapresultset = self.__lwscm_repository.find_all(word = word)
            for wcmap in wcmapresultset:
                if wcmap.category_id in wordcategorymap:
                    wordcategorymap[wcmap.category_id] += wcmap.score
                else:
                    wordcategorymap[wcmap.category_id] = wcmap.score

        categories = l0qh4.get('spendingcategories')

        if listallflag == True or len(wordcategorymap) == 0:
            categorydict = [ 
                    {"id": category.id, "name": category.name, "display_name": category.display_name}
                    for category in categories.listall()
            ]
        else:
            wordcategorymap = sorted(wordcategorymap.items(), reverse=True, key=lambda x: x[1])
            categorydict = [ 
                    {"id": category.id, "name": category.name, "display_name": category.display_name}
                    for category in categories.list_byids([ca[0] for ca in wordcategorymap])
            ]
        return categorydict

