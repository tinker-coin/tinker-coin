import logging
from random import random
from typing import Optional

from interface.iblockchainmanager import IBlockchainManager
from interface.icryptoprovider import ICryptoProvider
from interface.igossipmanager import IGossipManager
from interface.inetworkedworker import INetworkedWorker
from node.interface.iapp import IApp
from node.interface.iconfigprovider import IConfigProvider
from node.interface.irunnable import IRunnable
from node.datatypes.config import Config

logger = logging.getLogger(__name__)


class App(IRunnable, IApp):

    def __init__(self, working_dir: str, code_root: str):
        super().__init__()
        self.code_root = code_root
        self.working_dir = working_dir
        self.config_provider: Optional[IConfigProvider] = None
        self.crypto_provider: Optional[ICryptoProvider] = None
        self.ui_manager: Optional[INetworkedWorker] = None
        self.network_manager: Optional[INetworkedWorker] = None
        self.gossip_manager: Optional[IGossipManager] = None
        self.blockchain_manager: Optional[IBlockchainManager] = None

    def set_config_provider(self, config_provider: IConfigProvider):
        self.config_provider = config_provider

    def set_crypto_provider(self, crypto_provider: ICryptoProvider):
        self.crypto_provider = crypto_provider

    def set_ui_manager(self, ui_manager: INetworkedWorker):
        self.ui_manager = ui_manager

    def set_network_manager(self, network_manager: INetworkedWorker):
        self.network_manager = network_manager

    def set_gossip_manager(self, gossip_manager: IGossipManager):
        self.gossip_manager = gossip_manager

    def set_blockchain_manager(self, blockchain_manager: IBlockchainManager):
        self.blockchain_manager = blockchain_manager

    def start(self):
        """ Starts Application."""
        if self.config_provider is None:
            raise NotImplementedError("Config Provider not initialized.")
        if self.crypto_provider is None:
            raise NotImplementedError("Crypto Provider not initialized.")
        if self.ui_manager is None:
            raise NotImplementedError("UI Manager not initialized.")
        if self.network_manager is None:
            raise NotImplementedError("Network Manager not initialized.")
        if self.gossip_manager is None:
            raise NotImplementedError("Gossip Manager not initialized.")
        if self.blockchain_manager is None:
            raise NotImplementedError("Blockchain Manager not initialized.")
        if not self.check_sanity():
            return
        logger.info("Starting Tinker Node.")
        self.network_manager.bind(self.config_provider.get(Config.NETWORK_PORT),
                                  self.config_provider.get(Config.NETWORK_INTERFACE))
        self.network_manager.start()
        self.ui_manager.bind(self.config_provider.get(Config.UI_PORT),
                             self.config_provider.get(Config.UI_INTERFACE))
        self.ui_manager.start()
        self.gossip_manager.start()
        self.blockchain_manager.start()
        logger.info("Tinker Node UI started at %s", self.ui_manager.address())

    def check_sanity(self) -> bool:
        """ Checks sanity of config before starting."""
        logger.info("Checking Sanity.")
        if not self.config_provider.config_available():
            print("Config file not found!\n"
                  + "\tNew config file with default values will be created at: {}."
                  .format(self.config_provider.get_config_path()))
            if not _confirm():
                return False
        else:
            self.config_provider.load()
        if not self.config_provider.config_loaded():
            print("Config file not loaded properly!\n"
                  + "\tOverwrite config file with defaults at: {}."
                  .format(self.config_provider.get_config_path()))
            if not _confirm():
                return False
        if self.config_provider.get(Config.NETWORK_PORT) is None \
                or self.network_manager.is_port_in_use(self.config_provider.get(Config.NETWORK_PORT)):
            print("Network port not defined or is not available for use!\n"
                  + "\tA new random available port will be selected."
                  .format(self.config_provider.get_config_path()))
            if not _confirm():
                return False
            self.config_provider.set(Config.NETWORK_PORT, find_random_port(self.network_manager))
        if self.config_provider.get(Config.UI_PORT) is None \
                or self.ui_manager.is_port_in_use(self.config_provider.get(Config.UI_PORT)):
            print("UI port not defined or is not available for use!\n"
                  + "\tA new random available port will be selected."
                  .format(self.config_provider.get_config_path()))
            if not _confirm():
                return False
            self.config_provider.set(Config.UI_PORT,
                                     find_random_port(self.ui_manager,
                                                      exclude=[self.config_provider.get(Config.NETWORK_PORT)]))
            self.config_provider.save()
        return True


def find_random_port(worker: INetworkedWorker, exclude=None) -> Optional[int]:
    if exclude is None:
        exclude = []
    for retry in range(100):
        port = 2000 + int(random() * 50000)
        if port not in exclude and not worker.is_port_in_use(port):
            return port
    return None


def _confirm(message: str = "Do you want to continue? [y/N]") -> bool:
    print("{} ".format(message), end="")
    return input().lower().strip() == "y"
