import sys

import constants
from config import DefaultConfiguration
from driver import WebDriver
from logger import Logger
from twitter_news import TwitterNews

Logger.load()
args = sys.argv
config_file = ""
if len(args) != 3:
    Logger.error("Twitter's user and password needed")
    Logger.error("USAGE: python3 start.py <TWITTER_USER> <TWITTER_PASSWORD>")
    exit(1)
else:
    constants.USERNAME = args[1]
    constants.PASSWORD = args[2]


# Load config
config = DefaultConfiguration()
# DefaultConfiguration.load()

# Initializing the web driver
web_driver = WebDriver(config)

# Start the app
twitter = TwitterNews(web_driver, config)
twitter.start()

