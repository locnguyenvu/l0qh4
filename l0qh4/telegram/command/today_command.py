import l0qh4
import telegram

from ...repository.spendinglog_repository import SpendingLogRepository
from .command import Command

class TodayCommand(Command):

    def __init__(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))

    def process(self):
        logs = self._sl_repository.find_intimerange('today')
        totalamount = sum([ log.get_amount() for log in logs ])

        if self.hasOption('d') is True:
            users = l0qh4.get('users')
            spendingrows = [
                '[{}] {:10.10} | {:<3}'.format(
                    users.get_alias(telegram_username=log.get_created_by()),
                    log.get_subject(), 
                    log.get_amount(human_format=True)) 
                for log in logs
            ]

            self.reply(
                text = '\n'.join([
                        '```',
                        '\n'.join(spendingrows),
                        '{:=>20}'.format('='),
                        f'Tổng cộng: {totalamount:,}',
                        '```'
                    ]),
                parse_mode = telegram.ParseMode.MARKDOWN_V2)
            return
        else:
            self.reply(f'Tổng cộng hôm nay: {totalamount:,}')
            return

