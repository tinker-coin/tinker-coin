import logging
import socket
import threading
from http.server import BaseHTTPRequestHandler
from socketserver import BaseServer
from typing import Optional, Type

from interface.inetworkedworker import INetworkedWorker
from node.interface.iapp import IApp

logger = logging.getLogger(__name__)


class HTTPServer(INetworkedWorker):

    def __init__(self, http_server_class: Type[BaseServer], handler_class: Type[BaseHTTPRequestHandler]):
        self.http_server_class = http_server_class
        self.handler_class = handler_class
        self.binding_interface = None
        self.port = None
        self.app = None
        self._server = None
        self.running = False
        self._thread = threading.Thread(target=self.run)
        self._thread.deamon = True

    def set_app(self, app: IApp):
        self.app = app

    def bind(self, port: str, binding_interface: int):
        self.binding_interface = binding_interface
        self.port = port

    def is_port_in_use(self, port: int, binding_interface: Optional[str] = None) -> bool:
        binding_address = binding_interface if binding_interface is not None else "localhost"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((binding_address, port)) == 0

    def address(self) -> str:
        return "http://{}:{}/".format(
                    self.binding_interface if self.binding_interface != "" else "localhost",
                    self.port)

    def run(self):
        # noinspection HttpUrlsUsage
        logger.debug("Starting HTTP Server: %s", self.address())
        self.running = True
        self._server = self.http_server_class((self.binding_interface, self.port), self.handler_class)
        self._server.app = self.app
        while self.running:
            self._server.handle_request()
        logger.debug("HTTP Server at {} Terminated.", self.port)

    def start(self):
        self._thread.start()

    def stop(self):
        self.running = False

