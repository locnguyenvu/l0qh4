import l0qh4
import telegram

from .command import Command
from ...repository.spendinglog_repository import SpendingLogRepository

class ThismonthCommand(Command):

    def __init__(self):
        self._sl_repository = SpendingLogRepository(l0qh4.get('db'))

    def process(self):
        logs = self._sl_repository.find_intimerange('thismonth')
        totalamount = sum([ log.get_amount() for log in logs ])

        if self.hasOption('d') is False:
            self.reply(f'Tổng cộng tháng này: {totalamount:,}')
            return
        else:
            debit_amount = 0
            credit_amount = 0
            for log in logs:
                if log.get_transaction_type() == 'debit':
                    debit_amount += log.get_amount()
                elif log.get_transaction_type() == 'credit':
                    credit_amount += log.get_amount()

            self.reply(
                text = '\n'.join([
                        '```',
                        '{:6} {:>15,}'.format('Debit', debit_amount),
                        '{:6} {:>15,}'.format('Credit', credit_amount),
                        '{:=>20}'.format('='),
                        f'Tổng cộng: {totalamount:,}',
                        '```'
                    ]),
                parse_mode = telegram.ParseMode.MARKDOWN_V2)
