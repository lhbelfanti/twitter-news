import sys
from twitter_news import TwitterNews
from driver import WebDriverCreator
import constants
from config import Configuration
from logger import Logger


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


driver = WebDriverCreator().driver

# Load config
Configuration.load()

# Start the app
twitter = TwitterNews(driver)
twitter.start()

