from base64 import b64encode
from decimal import Decimal
from typing import Type

from datatypes.transactionoutputtype import TransactionOutputType


class TransactionOutput:

    def __init__(self,
                 amount: Type[Decimal],
                 transaction_type: Type[TransactionOutputType],
                 message: bytes
                 ):
        self.amount = amount
        self.transaction_type = transaction_type
        self.message = message

    def __dict__(self):
        return {
            "message": b64encode(self.message).decode('utf-8').rstrip("="),
            "transaction_type": self.transaction_type.value,
            "amount": str(self.amount)
        }
