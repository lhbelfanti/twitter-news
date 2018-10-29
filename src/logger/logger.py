from logging import getLogger

import logging

from pyfiglet import figlet_format


class Logger:
    loggers = {}

    @staticmethod
    def error(msg):
        logger = Logger.loggers.get('TWITTER_NEWS')
        logger.error(msg)

    @staticmethod
    def info(msg):
        logger = Logger.loggers.get('TWITTER_NEWS')
        logger.info(msg)

    @staticmethod
    def load():
        logger = getLogger('TWITTER_NEWS')

        logger.propagate = False

        logger.setLevel(logging.INFO)
        lh = logging.StreamHandler()
        lh.setLevel(logging.INFO)

        logger.addHandler(lh)

        logger.info(figlet_format("Twitter News", font="big", width=200))

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        lh.setFormatter(formatter)

        Logger.loggers['TWITTER_NEWS'] = logger


