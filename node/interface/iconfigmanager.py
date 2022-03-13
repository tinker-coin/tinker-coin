from node.types.config import Config


class IConfigManager:

    def load(self):
        """Loads config from persistent storage"""
        pass

    def save(self):
        """Saves config to persistent storage"""
        pass

    def config_available(self) -> bool:
        """Returns id config file is available or not"""
        pass

    def config_loaded(self) -> bool:
        """Returns if config file loaded successfully or not"""
        pass

    def get_config_path(self) -> str:
        """Returns persistent config store location"""
        pass

    def get(self, key: Config):
        """Returns """
        pass

    def set(self, key: Config, value):
        pass
