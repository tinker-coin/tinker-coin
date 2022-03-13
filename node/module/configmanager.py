import json
import logging
import os
from json import JSONDecodeError

from node.interface.iconfigmanager import IConfigManager
from node.types.config import Config

logger = logging.getLogger(__name__)


class ConfigManager(IConfigManager):

    def __init__(self, config_file_path: str):
        logger.debug("ConfigManager initialized with config path: %s", config_file_path)
        self._config_file_path = config_file_path
        self._loaded = False
        self._is_dirty = True
        self._config = self.default_config()

    @staticmethod
    def default_config():
        return {
            Config.NETWORK_NAME: "tinker-coin",
            Config.NETWORK_INTERFACE: "",
            Config.NETWORK_PORT: None,
            Config.UI_INTERFACE: "",
            Config.UI_PORT: None,
            Config.INCOMING_ADDRESSES: []
        }

    def config_available(self) -> bool:
        return os.path.exists(self.get_config_path())

    def get_config_path(self) -> str:
        return self._config_file_path

    def config_loaded(self) -> bool:
        return self._loaded

    def load(self):
        try:
            with open(self._config_file_path) as json_file:
                json_obj = json.load(json_file)
                config = {Config(k): v for k, v in json_obj.items() if Config.has_value(k)}
            self._config = {**self._config, **config}
            self._loaded = True
            self._is_dirty = False
            logger.debug("Config loaded: %s", self._config)
        except JSONDecodeError:
            pass

    def save(self):
        if not self._is_dirty:
            return
        logger.debug("Writing config: %s", self._config)
        with open(self._config_file_path, 'w') as outfile:
            json.dump({k.value: v for k, v in self._config.items()}, outfile, indent=4)
        self._loaded = True
        self._is_dirty = False

    def get(self, key: Config):
        return self._config[key]

    def set(self, key: Config, value):
        self._config[key] = value
        self._is_dirty = True

    def __repr__(self):
        return str(self._config)
