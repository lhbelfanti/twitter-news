import sys
import twitter_news
import constants
import utils

args = sys.argv
if len(args) != 3:
    utils.log("Twitter's user and password needed")
    exit(1)
else:
    constants.USERNAME = args[1]
    constants.PASSWORD = args[2]


twitter = twitter_news.TwitterNews()
twitter.start()
