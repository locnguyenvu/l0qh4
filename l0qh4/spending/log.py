import l0qh4

from pprint import pprint
from ..core import Base
from ..utils import StringUtil

class Log:

    def __init__(self, 
            subject: str, 
            amount: int, 
            payment_method: str, 
            transaction_type: str, 
            telegram_message_id: int, 
            created_by: str, 
            id = None, 
            spending_category_id = None, 
            created_at = None, 
            updated_at = None):
        self.__id = id
        self.__subject = subject
        self.__amount = amount
        self.__payment_method = payment_method
        self.__transaction_type = transaction_type
        self.__telegram_message_id = telegram_message_id
        self.__created_by = created_by 
        self.__spending_category_id = spending_category_id
        self.__created_at = created_at
        self.__updated_at = updated_at

    @classmethod
    def from_dict(cls, adict):
        return Log(
                id = adict['id'],
                subject = adict['subject'],
                amount = adict['amount'],
                payment_method = adict['payment_method'],
                transaction_type = adict['transaction_type'],
                telegram_message_id = adict['telegram_message_id'],
                created_by = adict['created_by'],
                spending_category_id = adict['spending_category_id'],
                created_at = adict['created_at'],
                updated_at = adict['updated_at'])

    def get_id(self):
        return self.__id

    def get_subject(self):
        return self.__subject

    def set_category_id(self, cateid:int):
        self.__spending_category_id = cateid

    def get_category_id(self):
        return self.__spending_category_id

    def get_amount(self):
        return self.__amount

    def get_payment_method(self):
        return self.__payment_method

    def get_transaction_type(self):
        return self.__transaction_type

    def get_subject_words(self):
        return StringUtil.split_to_words(self.__subject)

