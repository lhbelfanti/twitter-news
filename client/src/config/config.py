import json
from logger import Logger


class Configuration:
    config = {}

    @staticmethod
    def load(file_name):
        with open(file_name) as config_file:
            Logger.info("Loading configuration file.")
            Configuration.config = json.load(config_file)
            Logger.info("Configuration loaded.")
