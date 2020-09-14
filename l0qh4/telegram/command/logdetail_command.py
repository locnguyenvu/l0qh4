import l0qh4
import telegram

from .command import Command
from l0qh4.repository.spendinglog_repository import SpendingLogRepository

class LogDetailCommand(Command):

    def process(self):

        sl_repository = SpendingLogRepository(l0qh4.get('db'))
        spendingcategories = l0qh4.get('spendingcategories')

        log = sl_repository.find_first(
                telegram_message_id=self.update.message.reply_to_message.message_id)

        self.reply(
                text = '\n'.join([
                        '```',
                        '{:4} {}'.format('#id', log.get_id()),
                        '{:4} {}'.format('sbj', log.get_subject()),
                        '{:4} {}'.format('amt', log.get_amount(human_format=True)),
                        '{:4} {:}'.format('cat', log.get_category_name()),
                        '```'
                    ]),
                parse_mode = telegram.ParseMode.MARKDOWN_V2)
