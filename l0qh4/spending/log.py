import l0qh4

from ..shared.domain_model import DomainModel
from ..utils import NumberUtil, StringUtil

class Log(DomainModel):

    def __init__(self, 
            id = None, 
            subject: str = None, 
            amount: int = None, 
            payment_method: str = None, 
            transaction_type: str = None, 
            telegram_message_id: int = None, 
            created_by: str = None, 
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

    def get_id(self):
        return self.__id

    def set_id(self, id: int):
        self.__id = id

    def get_subject(self):
        return self.__subject

    def set_subject(self, subject:str):
        self.__subject = subject

    def get_amount(self, human_format=False):
        if human_format is True:
            return NumberUtil.human_format(self.__amount)
        return self.__amount

    def set_amount(self, amount:int):
        self.__amount = amount

    def set_category_id(self, cateid:int):
        self.__spending_category_id = cateid

    def get_category_id(self):
        return self.__spending_category_id

    def get_payment_method(self):
        return self.__payment_method

    def set_payment_method(self, paymentmethod: str):
        self.__payment_method = paymentmethod

    def get_transaction_type(self):
        return self.__transaction_type

    def set_transaction_type(self, transactiontype: str):
        self.__transaction_type = transactiontype

    def get_telegram_message_id(self):
        return self.__telegram_message_id

    def get_created_by(self):
        return self.__created_by

    def get_created_at(self):
        return self.__created_at

    def get_updated_at(self):
        return self.__updated_at

    def get_subject_words(self):
        return StringUtil.split_to_words(self.__subject)

    def get_category(self):
        categories = l0qh4.get('spendingcategories')
        return categories.get(self.get_category_id())

    def get_category_name(self):
        cat = self.get_category()
        return cat.display_name if cat.display_name is not None else cat.name

