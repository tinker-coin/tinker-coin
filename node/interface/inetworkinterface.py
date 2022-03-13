from typing import Optional


class INetworkInterface:

    def bind(self, port: int, binding_interface: str):
        """ Bind to a network interface. """
        pass

    def is_port_in_use(self, port: int, binding_interface: Optional[str] = None) -> bool:
        """ Test if port is in use. """
        pass
