import l0qh4
import telegram

from .command import Command

class ListCategoryCommand(Command):

    def process(self):
        categories = l0qh4.get('spendingcategories').listall()
        content = [ 
                f'{cate.id:2} {cate.name:10}'
                for cate in categories
        ]
        self.reply('\n'.join(['```', '\n'.join(content), '```']), parse_mode = telegram.ParseMode.MARKDOWN_V2)
