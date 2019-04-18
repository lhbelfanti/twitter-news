import sys

import json
import constants
from logger import Logger
from twitter_news import TwitterNews
from di import Injector

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

# Initialize the Injector
with open(constants.DI_JSON) as config_file:
    config = json.load(config_file)
inj = Injector(config)
inj.load()

# Start the app
twitter = TwitterNews(inj)
twitter.start()
