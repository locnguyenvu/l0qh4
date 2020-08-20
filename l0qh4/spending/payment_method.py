from enum import Enum

class TransactionType(Enum):
    DEBIT = 'debit'
    CREDIT = 'credit'
    EWALLET = 'ewaller'

class PaymentMethod(Enum):
    CASH = 'cash'
    # Debit cards
    VIB = 'vib'
    # Mobile money
    MOMO = 'momo'
    VIETTELPAY = 'viettelpay'
    # Credit cards
    CREDIT_CITIBANK = 'credit_citibank'
    CREDIT_TIKISACOMBANK = 'credit_tikisacombank'

    def type(self) -> str:
        if self in [self.CREDIT_TIKISACOMBANK, self.CREDIT_CITIBANK]:
            return TransactionType.CREDIT.value
        elif self in [self.MOMO, self.VIETTELPAY]:
            return TransactionType.EWALLET.value
        return TransactionType.DEBIT.value

