import os
import json
from logger import Logger


class Configuration:
    config = {}

    @staticmethod
    def load():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.json'))
        with open(path) as config_file:
            Logger.info("Loading configuration file.")
            Configuration.config = json.load(config_file)
            Logger.info("Configuration loaded.")
