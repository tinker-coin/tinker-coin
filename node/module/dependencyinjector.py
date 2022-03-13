import socketserver

from interface.iapp import IApp
from interface.iconfigmanager import IConfigManager
from interface.inetworkedworker import INetworkedWorker
from module.app import App
from module.configmanager import ConfigManager
from module.httpserver import HTTPServer
from module.networkrequesthandler import NetworkRequestHandler
from node.types.singleton import Singleton
from module.uirequesthandler import UIRequestHandler


class DependencyInjector(metaclass=Singleton):
    """ This module creates instances of all dependent modules and maintain dependency between them."""
    def __init__(self, config_file: str):
        self.config_file = config_file
        # initialize objects
        self._app = App()
        self._config_manager = ConfigManager(self.config_file)
        self._ui_manager = HTTPServer(http_server_class=socketserver.TCPServer,
                                      handler_class=UIRequestHandler)
        self._network_manager = HTTPServer(http_server_class=socketserver.TCPServer,
                                           handler_class=NetworkRequestHandler)
        # connect dependencies
        self._app.set_config_manager(self._config_manager)
        self._app.set_ui_manager(self._ui_manager)
        self._app.set_network_manager(self._network_manager)
        self._ui_manager.set_app(self._app)
        self._network_manager.set_app(self._app)

    @property
    def app(self) -> IApp:
        return self._app

    @property
    def config_manager(self) -> IConfigManager:
        return self._config_manager

    @property
    def ui_manager(self) -> INetworkedWorker:
        return self._ui_manager

    @property
    def network_manager(self) -> INetworkedWorker:
        return self._network_manager
