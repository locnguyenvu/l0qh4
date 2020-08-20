import re

from .payment_method import PaymentMethod

class LogMessage:

    """ Spending log source from telegram message"""

    def __init__(self, content):
        self.content = content
        self.__payment_method = PaymentMethod.CASH
        self.__spending_amount = None
        self.__spending_subject = None
        self.tokenize()

    def tokenize(self):
        tokens = self.content.split(' ')
        regex_spending_amount = re.compile(r'\d+(k|$)')
        # Find payment_method
        pmet = tokens[-1]
        try: 
            self.__payment_method = PaymentMethod(pmet)
            tokens.pop()
        except ValueError:
            self.__payment_method = PaymentMethod('cash')
            if not regex_spending_amount.match(pmet):
                tokens.pop()

        # Find spending amount
        for i in reversed(range(len(tokens))):
            spendingamount = tokens[i].lower()
            if regex_spending_amount.match(spendingamount):
                spendingamount = re.sub('k$', '000', spendingamount).strip()
                self.__spending_amount = int(spendingamount)
                tokens.pop(i)
                break

        # Spending subject
        self.__spending_subject = ' '.join(tokens)

    def payment_method(self):
        return self.__payment_method.value

    def transaction_type(self):
        return self.__payment_method.type()

    def amount(self):
        return self.__spending_amount

    def subject(self):
        if re.match('^/log', self.__spending_subject):
            subject = self.__spending_subject[len('/log')+1:]
        else:
            subject = self.__spending_subject
        return subject 

    def is_valid(self):
        return self.__spending_amount is not None

