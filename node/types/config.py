from enum import Enum


class Config(Enum):
    """List of available configurations."""
    NETWORK_NAME = "network_name"
    NETWORK_INTERFACE = "network_interface"
    NETWORK_PORT = "network_port"
    UI_INTERFACE = "ui_interface"
    UI_PORT = "ui_port"
    INCOMING_ADDRESSES = "incoming_addresses"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
