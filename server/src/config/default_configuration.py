import os
import json
import constants

from logger import Logger
from config import Configuration


class DefaultConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        self._config = {}
        self._common = constants.COMMON
        self._ui_version = self._common

    def _define_dependencies(self):
        pass

    def construct(self, dependencies):
        self.load()

    def load(self, data=None):
        if data is not None:
            self._config = data
            return

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), constants.CONFIGS_PATH))
        with open(path) as configs_file:
            Logger.info("Loading configuration files.")
            configs = json.load(configs_file)
            for config in configs:
                config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), configs[config]))
                with open(config_path) as config_file:
                    Logger.info("Loading " + config + "...")
                    config_data = json.load(config_file)
                    self._config[config] = config_data

            Logger.info("Configurations loaded.")

    def define_twitter_ui_version(self, url):
        if url == "https://twitter.com/":
            self._ui_version = constants.V1
        elif url == "https://twitter.com/home":
            self._ui_version = constants.V2

    def ui_version(self, version):
        return self._ui_version == version

    def get_prop(self, prop, config=constants.SE_CFG):
        # Selenium Configuration
        if config == constants.SE_CFG:
            data = self._config[config]
            if prop in data[self._ui_version]:
                return data[self._ui_version][prop]
            elif prop in data[self._common]:
                return data[self._common][prop]
            else:
                return ""

        # Default Configuration
        return self._config[config][prop]

