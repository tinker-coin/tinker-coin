import abc

from interface.irunnable import IRunnable


class IBlockchainManager(IRunnable, metaclass=abc.ABCMeta):
    pass
