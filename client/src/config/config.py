import json
from logger import Logger


class Configuration:
    config = {}

    @staticmethod
    def load():
        with open("config.json") as config_file:
            Logger.info("Loading configuration file.")
            Configuration.config = json.load(config_file)
            Logger.info("Configuration loaded.")
