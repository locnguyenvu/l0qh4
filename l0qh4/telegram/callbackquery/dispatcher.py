import l0qh4

from .mapslcategory_callbackquery import MapSlCategoryCallbackQuery

class Dispatcher(object):
    
    def __call__(self, update, context):
        self.update = update
        self.context = context 

        callbackargumments = self.update.callback_query.data.split('|')

        handlername = callbackargumments[0]
        params = dict()
        for ptparam in callbackargumments[1].split(','):
            key, value = tuple(ptparam.split('='))
            params[key] = value

        if handlername == 'MapSlCategoryCallbackQuery':
            handler = MapSlCategoryCallbackQuery(update, context)
            handler.execute(**params)

        self.update.callback_query.answer()
