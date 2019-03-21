import os
import json
import constants

from logger import Logger
from config import Configuration


class DefaultConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        self._config = {}

    def _define_dependencies(self):
        pass

    def construct(self, dependencies):
        self._load()

    def _load(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), constants.CONFIG_PATH))
        with open(path) as config_file:
            Logger.info("Loading configuration file.")
            self._config = json.load(config_file)
            Logger.info("Configuration loaded.")

    def get(self, prop):
        return self._config[prop]

