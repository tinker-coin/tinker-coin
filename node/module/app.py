import logging
from random import random
from typing import Optional

from interface.inetworkedworker import INetworkedWorker
from node.interface.iapp import IApp
from node.interface.iconfigmanager import IConfigManager
from node.interface.irunnable import IRunnable
from node.types.config import Config

logger = logging.getLogger(__name__)


class App(IRunnable, IApp):

    def __init__(self):
        self.network_manager: Optional[INetworkedWorker] = None
        self.ui_manager: Optional[INetworkedWorker] = None
        self.config_manager: Optional[IConfigManager] = None

    def set_config_manager(self, config_manager: IConfigManager):
        self.config_manager = config_manager

    def set_network_manager(self, network_manager: INetworkedWorker):
        self.network_manager = network_manager

    def set_ui_manager(self, ui_manager: INetworkedWorker):
        self.ui_manager = ui_manager

    def start(self):
        """ Starts Application."""
        if self.config_manager is None:
            raise NotImplementedError("Config Manager not provided.")
        if self.network_manager is None:
            raise NotImplementedError("Network Manager not provided.")
        if self.ui_manager is None:
            raise NotImplementedError("UI Manager not provided.")
        if not self.check_sanity():
            return
        logger.info("Starting Tinker Node.")
        self.network_manager.bind(self.config_manager.get(Config.NETWORK_PORT),
                                  self.config_manager.get(Config.NETWORK_INTERFACE))
        self.network_manager.start()
        self.ui_manager.bind(self.config_manager.get(Config.UI_PORT),
                             self.config_manager.get(Config.UI_INTERFACE))
        self.ui_manager.start()

    def check_sanity(self) -> bool:
        """ Checks sanity of config before starting."""
        logger.info("Checking Sanity.")
        if not self.config_manager.config_available():
            print("Config file not found!\n"
                  + "\tNew config file with default values will be created at: {}."
                  .format(self.config_manager.get_config_path()))
            if not _confirm():
                return False
        else:
            self.config_manager.load()
        if not self.config_manager.config_loaded():
            print("Config file not loaded properly!\n"
                  + "\tOverwrite config file with defaults at: {}."
                  .format(self.config_manager.get_config_path()))
            if not _confirm():
                return False
        if self.config_manager.get(Config.NETWORK_PORT) is None \
                or self.network_manager.is_port_in_use(self.config_manager.get(Config.NETWORK_PORT)):
            print("Network port not defined or is not available for use!\n"
                  + "\tA new random available port will be selected."
                  .format(self.config_manager.get_config_path()))
            if not _confirm():
                return False
            self.config_manager.set(Config.NETWORK_PORT, find_random_port(self.network_manager))
        if self.config_manager.get(Config.UI_PORT) is None \
                or self.ui_manager.is_port_in_use(self.config_manager.get(Config.UI_PORT)):
            print("UI port not defined or is not available for use!\n"
                  + "\tA new random available port will be selected."
                  .format(self.config_manager.get_config_path()))
            if not _confirm():
                return False
            self.config_manager.set(Config.UI_PORT,
                                    find_random_port(self.ui_manager,
                                                     exclude=[self.config_manager.get(Config.NETWORK_PORT)]))
            self.config_manager.save()
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
