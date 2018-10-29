import sys

import twitter_news
import constants
from logger import Logger


Logger.load()
args = sys.argv
if len(args) != 3:
    Logger.error("Twitter's user and password needed")
    Logger.error("USAGE: python3 start.py <TWITTER_USER> <TWITTER_PASSWORD>")
    exit(1)
else:
    constants.USERNAME = args[1]
    constants.PASSWORD = args[2]


twitter = twitter_news.TwitterNews()
twitter.start()
