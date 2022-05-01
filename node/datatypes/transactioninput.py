from base64 import b64encode


class TransactionInput:
    def __init__(self,
                 block_id: bytes,
                 transaction_id: bytes,
                 output_index: int
                 ):
        self.block_id = block_id
        self.transaction_id = transaction_id
        self.output_index = output_index

    def __dict__(self):
        return {
            "block_id": b64encode(self.block_id).decode('utf-8').rstrip("="),
            "transaction_id": b64encode(self.transaction_id).decode('utf-8').rstrip("="),
            "output_index": str(self.output_index)
        }
