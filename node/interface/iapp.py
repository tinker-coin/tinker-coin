import abc

from interface.irunnable import IRunnable


class IApp(IRunnable, metaclass=abc.ABCMeta):

    def __int__(self):
        self.code_root = None
        self.working_dir = None
        self.config_provider = None
        self.crypto_provider = None
        self.ui_manager = None
        self.network_manager = None
        self.gossip_manager = None
        self.blockchain_manager = None



