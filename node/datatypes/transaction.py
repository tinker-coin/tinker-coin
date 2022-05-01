from typing import List, Type

from constants.tinkerconstants import TINKER_TRANSACTION_VERSION
from datatypes.tinkertimestamp import TinkerTimestamp
from datatypes.transactioninput import TransactionInput
from datatypes.transactionoutput import TransactionOutput
from datatypes.transactiontype import TransactionType


class Transaction:

    def __init__(self,
                 time_stamp: TinkerTimestamp = TinkerTimestamp.now(),
                 version: int = TINKER_TRANSACTION_VERSION,
                 transaction_type: Type[TransactionType] = TransactionType.Transfer,
                 inputs: List[Type[TransactionInput]] = None,
                 outputs: List[Type[TransactionOutput]] = None
                 ):
        self.time_stamp = time_stamp
        self.version = version
        self.transaction_type = transaction_type
        self.inputs = inputs if inputs else []
        self.outputs = outputs if outputs else []

    def add_input(self, i: Type[TransactionInput]):
        self.inputs.append(i)

    def add_outputs(self, o: Type[TransactionOutput]):
        self.outputs.append(o)

    def __dict__(self):
        return {
            "outputs": [o.__dict__ for o in self.outputs],
            "inputs": [i.__dict__ for i in self.inputs],
            "version": str(self.version),
            "transaction_type": self.transaction_type.value,
            "time_stamp": str(self.time_stamp.to_ordinal)
        }
