import abc


class ICryptoProvider(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_wallet(self, passcode: str):
        pass

