import l0qh4
import telegram

from ...repository.spendinglog_repository import SpendingLogRepository
from .command import Command

class TodayCommand(Command):

    def __init__(self, show_detail=False):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))
        self._showdetail = show_detail 

    def process(self):
        logs = self._sl_repository.find_intimerange('today')
        totalamount = sum([ log.get_amount() for log in logs ])

        if self._showdetail is False:
            self.reply(f'Tổng cộng hôm nay: {totalamount:,}')
        else:
            spendingrows = [
                '{:10.10} | {:<3}'.format(
                    log.get_subject(), 
                    log.get_amount(human_format=True)) 
                for log in logs
            ]

            self.reply(
                text = '\n'.join([
                        '```',
                        '\n'.join(spendingrows),
                        '{:=>20}'.format('='),
                        f'Tổng cộng hôm nay: {totalamount:,}',
                        '```'
                    ]),
                parse_mode = telegram.ParseMode.MARKDOWN_V2)
