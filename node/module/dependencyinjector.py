import socketserver
from typing import Optional

from interface.iapp import IApp
from module.app import App
from module.blockchainmanager import BlockchainManager
from module.configprovider import ConfigProvider
from module.cryptoprovider import CryptoProvider

from module.gossipmanager import GossipManager
from module.httpserver import HTTPServer
from module.networkrequesthandler import NetworkRequestHandler
from node.datatypes.singleton import Singleton
from module.uirequesthandler import UIRequestHandler


class DependencyInjector(metaclass=Singleton):
    """ This module creates instances of all dependent modules and maintain dependency between them."""
    def __init__(self, config_file: str, working_dir: str, code_root: str):
        self.code_root = code_root
        self.working_dir = working_dir
        self.config_file = config_file
        self._app: Optional[App] = None
        self._config_provider: Optional[ConfigProvider] = None
        self._crypto_provider: Optional[CryptoProvider] = None
        self._ui_manager: Optional[HTTPServer] = None
        self._network_manager: Optional[HTTPServer] = None
        self._blockchain_manager: Optional[BlockchainManager] = None
        self._gossip_manager: Optional[GossipManager] = None
        self.initialize = False

    def initialize_objects(self):
        # initialize objects
        self._app = App(working_dir=self.working_dir, code_root=self.code_root)
        self._config_provider = ConfigProvider(self.config_file)
        self._crypto_provider = CryptoProvider()
        self._ui_manager = HTTPServer(http_server_class=socketserver.TCPServer,
                                      handler_class=UIRequestHandler)
        self._network_manager = HTTPServer(http_server_class=socketserver.TCPServer,
                                           handler_class=NetworkRequestHandler)
        self._blockchain_manager = BlockchainManager()
        self._gossip_manager = GossipManager()
        # connect dependencies
        self._app.set_config_provider(self._config_provider)
        self._app.set_crypto_provider(self._crypto_provider)
        self._app.set_ui_manager(self._ui_manager)
        self._app.set_network_manager(self._network_manager)
        self._app.set_blockchain_manager(self._blockchain_manager)
        self._app.set_gossip_manager(self._gossip_manager)

        self._ui_manager.set_app(self._app)
        self._network_manager.set_app(self._app)
        self._blockchain_manager.set_app(self._app)
        self._gossip_manager.set_app(self._app)

        self.initialize = True

    @property
    def app(self) -> IApp:
        if not self.initialize:
            self.initialize_objects()
        return self._app
